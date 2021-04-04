import mensagem_pb2
from socket import *

import mysql.connector 

db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
  database="sistemaProvas",
  auth_plugin='mysql_native_password'
)


# Tipos de Status
class CodigosStatus():
    auth_success = [10,"login success"]
    auth_failed = [11,"login failed"]
    auth_online = [12,"already logged"]
    logout = [13,"logout success"]
    resposta_armazenada = [14,"resposta armazenada"]

# Realiza autenticação
def autenticacao(login, senha):
    # Consulta ao banco
    mycursor = db.cursor()
    mycursor.execute("SELECT login,senha,token,ativo FROM Aluno WHERE login = \'"+login+"\'")
    myresult = mycursor.fetchall()

    # Mensagem de Status
    status = mensagem_pb2.STATUS()
    # Mensagem de ACK_LOGIN
    ack_login = mensagem_pb2.ACK_LOGIN()
    # Mensagem do tipo MESNAGEM()
    msg_ack_login = mensagem_pb2.MENSAGEM()

    if len(myresult) == 0:
        status.codigo = CodigosStatus.auth_failed[0]
        status.descricao = CodigosStatus.auth_failed[1]
        ack_login.token = ''
        ack_login.status.codigo = status.codigo
        ack_login.status.descricao = status.descricao
    else:
        consulta = myresult[0]
        if consulta[3] == 1:
            status.codigo = CodigosStatus.auth_online[0]
            status.descricao = CodigosStatus.auth_online[1]
            ack_login.token = ''
            ack_login.status.codigo = status.codigo
            ack_login.status.descricao = status.descricao
        else:
            if (consulta[0] == login) & (consulta[1] == senha):
                status.codigo = CodigosStatus.auth_success[0]
                status.descricao = CodigosStatus.auth_success[1]
                ack_login.token = consulta[2]
                ack_login.status.codigo = status.codigo
                ack_login.status.descricao = status.descricao
                mycursor = db.cursor()
                sql = "UPDATE Aluno SET ativo = 1 WHERE login = \'"+consulta[0]+"\'"
                mycursor.execute(sql)
                db.commit()
            else:
                status.codigo = CodigosStatus.auth_failed[0]
                status.descricao = CodigosStatus.auth_failed[1]
                ack_login.token = ''
                ack_login.status.codigo = status.codigo
                ack_login.status.descricao = status.descricao

    msg_ack_login.acklogin.token = ack_login.token
    msg_ack_login.acklogin.status.codigo = ack_login.status.codigo
    msg_ack_login.acklogin.status.descricao = ack_login.status.descricao

    return msg_ack_login
    
# Realiza logout
def logout(token):
    mycursor = db.cursor()
    sql = "UPDATE Aluno SET ativo = 0 WHERE token = \'"+token+"\'"
    mycursor.execute(sql)
    db.commit()
    log = mensagem_pb2.LOGOUT()
    log.token = "ok"
    msg = mensagem_pb2.MENSAGEM()
    msg.logout.token = log.token
    return msg


# Realiza entrega da prova
def ACK_prova(token,idProva):
    
    # Listando questões da prova
    mycursor = db.cursor()
    mycursor.execute("SELECT id,ponto,enunciado FROM Questao WHERE codigoProva = \'"+idProva+"\'")
    questoes = mycursor.fetchall()
   
    
    # Listando alternativas de cada questão
    alternativas = []
    for q in questoes:
        mycursor.execute("SELECT descricao,codigo,idQuestao FROM Alternativa where idQuestao = "+str(q[0]))
        alternativas.append(mycursor.fetchall())

    # Preparando mensagem ACK_REQ_PROVA
    ack_req_prova = mensagem_pb2.ACK_REQ_PROVA()
    ack_req_prova.id_prova = idProva

    lista_aux_alternativas = [] # Lista auxiliar para armazenar as mensagens PB da alternativas de determinada questao
    lista_mensagens_alternativas = []

    # Criando uma lista composta por listas de ALTERNATIVAS
    for a in alternativas:
        for unica_alternativa in a:
            alt = mensagem_pb2.Alternativa()
            alt.descricao = unica_alternativa[0]
            alt.codigo = unica_alternativa[1]
            lista_aux_alternativas.append(alt)
        
        lista_mensagens_alternativas.append(lista_aux_alternativas)
        lista_aux_alternativas = []

    # Criando uma lista de QUESTAO
    lista_mensagens_questoes = []
    for i in range(0,len(questoes)):
        questao = mensagem_pb2.QUESTAO()
        q = questoes[i]
        questao.id = q[0]
        questao.enunciado = q[2]
        questao.pontos = q[1]
        for a in lista_mensagens_alternativas[i]:
            questao.alternativas.append(a)
        
        lista_mensagens_questoes.append(questao)
   
    # Criando mensagem ACK_REQ_PROVA
    for q in lista_mensagens_questoes:
        ack_req_prova.questoes.append(q)
    

    msg = mensagem_pb2.MENSAGEM()
    msg.ackreqprova.id_prova = ack_req_prova.id_prova
    for x in ack_req_prova.questoes:
        msg.ackreqprova.questoes.append(x)

 
    return msg # Enviar mensagem
    

# Armazena repostas do usuário
def armazena_respostas(msg_rx):

    respostas = msg_rx.SerializeToString() # ProtocolBuffer to bytes
    respostas_string = respostas.decode("utf-8") # bytes to string
    #b = str.encode(s) # voltando para bytes (só realizar parse)
    token = msg_rx.reqresp.token
    id_prova = msg_rx.reqresp.id_prova
    
    # Armazenando prova
    mycursor = db.cursor()
    sql = "INSERT INTO Aluno_Prova (tokenAluno, codigoProva, respostas) VALUES (%s, %s, %s)"
    val = (token, id_prova, respostas)
    mycursor.execute(sql, val)
    db.commit()

    status = mensagem_pb2.STATUS()
    status.codigo = CodigosStatus.resposta_armazenada[0]
    status.descricao = CodigosStatus.resposta_armazenada[1]
    msg = mensagem_pb2.MENSAGEM()
    msg.status.codigo = status.codigo
    msg.status.descricao = status.descricao
    return msg
    
# Realiza correção da prova
def correcao_prova(msg_rx):

    token = msg_rx.reqresultado.token
    id_prova = msg_rx.reqresultado.id_prova

    # Retirando do banco resposta armazenada
    mycursor = db.cursor()
    mycursor.execute("SELECT respostas FROM Aluno_Prova WHERE codigoProva = \'"+str(id_prova)+"\' AND tokenAluno = \'"+token+"\'")
    respostas_certas = mycursor.fetchall()
    a = respostas_certas[0]         # String
    b = str.encode(a[0])            # Bytes
    m = mensagem_pb2.MENSAGEM()
    m.ParseFromString(b)            # Bytes to ProtocolBuffer
    
    token = m.reqresp.token
    id_prova = m.reqresp.id_prova
    respostas = m.reqresp.respostas
    nota = 0
    correcao = True
    lista_resultados = [] # Lista de resultados
   

    for r in respostas: # Respostas do cliente [id:x codigos{ codgigos: 'v3p1'}, ]
        if r.WhichOneof('resp') == 'texto':
            print('resposta texto')
        else:
            mycursor = db.cursor()
            mycursor.execute("SELECT codigoAlternativa FROM Resposta WHERE idQuestao = "+str(r.id))
            respostas_certas = mycursor.fetchall() # Lista de repostas certas para cada questão
            result = mensagem_pb2.RESULTADO()      # Mensagem de RESULTADO

            if len(r.codigos.codigos) != len(respostas_certas): 
                result.questao = r.id
                result.pontos = 0
                lista_resultados.append(result)
            else:
                for i in range(0,len(respostas_certas)):
                    correcao = True
                    rpc = respostas_certas[i]                  # Cada uma das repostas certas vindas do banco [(a,),(b,)]
                    if rpc[0] != r.codigos.codigos[i]:         # Verifica com reposta do usuário, se uma for diferente já errou 
                        correcao = False

                if correcao:
                    mycursor.execute("SELECT ponto FROM Questao WHERE id = "+str(r.id))
                    p = mycursor.fetchall()
                    ponto = p[0]
                    nota += int(ponto[0])
                    result.questao = r.id
                    result.pontos = ponto[0]
                    lista_resultados.append(result)
                else:
                    result.questao = r.id
                    result.pontos = 0
                    lista_resultados.append(result)
                

    ack_resultado = mensagem_pb2.ACK_REQ_RESULTADO()
    ack_resultado.id_prova = id_prova
    ack_resultado.nota = nota
    for i in lista_resultados:
        ack_resultado.questoes.append(i)

    # Mensagem do tipo MENSAGEM
    msg = mensagem_pb2.MENSAGEM()
    msg.ackreqresultado.id_prova = ack_resultado.id_prova
    msg.ackreqresultado.nota = ack_resultado.nota

    for i in ack_resultado.questoes:
        msg.ackreqresultado.questoes.append(i)

    return msg

# Verifica tipo de mensagem recebida
def verifica_mensagem(msg_rx):
    if msg_rx.WhichOneof('msg') == 'login':
        return autenticacao(msg_rx.login.login,msg_rx.login.senha)
    elif msg_rx.WhichOneof('msg') == 'logout':
        return logout(msg_rx.logout.token)
    elif msg_rx.WhichOneof('msg') == 'reqprova':
        return ACK_prova(msg_rx.reqprova.token,msg_rx.reqprova.id_prova)
    elif msg_rx.WhichOneof('msg') == 'reqresp':
        return armazena_respostas(msg_rx)
    elif msg_rx.WhichOneof('msg') == 'reqresultado':
        return correcao_prova(msg_rx)
    else:
        print('erro')


# Configuração do Socket 
sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
sock.bind(('127.0.0.1', 9000))
sock.listen(5)
conn, addr = sock.accept()

if __name__ == "__main__":
    print("Servidor no ar...")
    
    while(True):
        
        data = conn.recv(1024)

        # Transformando para ProtocolBuffer
        msg_rx = mensagem_pb2.MENSAGEM()
        msg_rx.ParseFromString(data)
      
        conn.send(verifica_mensagem(msg_rx).SerializeToString())
    
    









