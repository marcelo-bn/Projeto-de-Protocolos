import mensagem_pb2
from socket import *

s = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
s.connect(('127.0.0.1', 9000))

def recebe():
    m = s.recv(1024)
    # Transformando para ProtocolBuffer
    msg_rx = mensagem_pb2.MENSAGEM()
    msg_rx.ParseFromString(m)
    return msg_rx

def envia(data):
    s.send(data)
    return recebe()
  
# Realiza autenticação
def autenticacao(login,senha):

    # Prepara e envia mensagem
    aut = mensagem_pb2.LOGIN()
    aut.login = login
    aut.senha = senha
    msg = mensagem_pb2.MENSAGEM()
    msg.login.login = aut.login
    msg.login.senha = aut.senha
    data = msg.SerializeToString()
    
    mensagem = envia(data)
 
    # Analisa resposta
    if mensagem.acklogin.status.codigo == 10:
        return mensagem.acklogin.token
    elif mensagem.acklogin.status.codigo == 12:
        return 'already'
    else:
        return "erro"

# Realiza Logout
def logout(token):

    # Prepara e envia mensagem
    log = mensagem_pb2.LOGOUT()
    log.token = token
    msg = mensagem_pb2.MENSAGEM()
    msg.logout.token = log.token
    data = msg.SerializeToString()
    
    resposta = envia(data)

    return resposta

# Realiza requisição de prova
def requisicao_prova(token, idProva):
    req_prova = mensagem_pb2.REQ_PROVA()
    req_prova.token = token
    req_prova.id_prova = idProva
    msg = mensagem_pb2.MENSAGEM()
    msg.reqprova.token = req_prova.token
    msg.reqprova.id_prova = req_prova.id_prova 
    data = msg.SerializeToString()

    resposta = envia(data)

    return resposta

# Envia respostas
def enviando_resposta(lista_idQuestao, lista_alternativas, toke, idProva):
    id_questao = [1,2]
    id_alternativas = [['v3p1'],['v4p1','v5p1']]

    # Mensagem REQ_RESP
    resposta_prova = mensagem_pb2.REQ_RESP()
    resposta_prova.token = token
    resposta_prova.id_prova = idProva

    # Lista de RESPOSTAS
    lista_msg_resposta = []

    for r in range(0,len(lista_idQuestao)):      
        rsp = mensagem_pb2.RESPOSTA()            # Cria objeto resposta
        rsp.id = lista_idQuestao[r]              # Armazena a questão da lista_idQuestao
        for alt in lista_alternativas[r]:
            rsp.codigos.codigos.append(alt)     # Arnazena as alternativas escolhidas dessa questão
        
        resposta_prova.respostas.append(rsp)     # Armazena um mensagem RESPOSTA em REQ_RESP

    # Mensagem do tipo MENSAGEM
    msg = mensagem_pb2.MENSAGEM()
    msg.reqresp.token = resposta_prova.token 
    msg.reqresp.id_prova = resposta_prova.id_prova
    for i in range(0,len(resposta_prova.respostas)):
        msg.reqresp.respostas.append(resposta_prova.respostas[i])     # Armazenando as mensagens do tipo REQ_RESP

    data = msg.SerializeToString()
    resposta = envia(data)
    
    return True

# Requisiçao do resultado
def requisicao_resultado(token, idProva):
    r = mensagem_pb2.REQ_RESULTADO()
    r.token = token
    r.id_prova = idProva
    msg = mensagem_pb2.MENSAGEM()
    msg.reqresultado.token = r.token
    msg.reqresultado.id_prova = r.id_prova
    data = msg.SerializeToString()

    resposta = envia(data)

    return resposta
    
if __name__ == "__main__":
    
    while True:
        auth = True
        token = ''
        
        while auth:
            login = input('> Insira o seu login: ')
            senha = input('> Insira a sua senha: ')
            r = autenticacao(login,senha)
            if r != 'erro':
                token = r
                auth = False
            

        print("Seu token é: "+token)
        auth = True
        lista_idQuestao = []
        lista_alternativas = []

        while auth:
            op = -1
            print('> 1 - Iniciar prova.')
            print('> 2 - Sair da sua conta.')
            op = int(input('> Insira uma opção: '))

            if op == 1:

                idProva = input('> Insira o id da prova fornecido pelo seu professor: ')
                r = requisicao_prova(token, idProva)
                print("\n")

                # Apresenta questões e alternativas
                for q in r.ackreqprova.questoes:
                    print(q.id,"-",q.enunciado,"(",q.pontos,"pontos)")
                    lista_idQuestao.append(q.id)
                    for a in q.alternativas:
                        print(a.codigo,"-",a.descricao)

                print("\n> Responda as questões: ")    
                # Armazena respostas
                for q in r.ackreqprova.questoes:
                    lista_aux_alternativas =[]
                    print("> Questão",q.id)
                    o = ""
                    while o!="sair":
                        o = input("> Digite o código da alternativa ou [sair] para ir para a próxima questão: ")
                        if o != "sair":
                            lista_aux_alternativas.append(o)
                    lista_alternativas.append(lista_aux_alternativas)


                op1 = int(input('\n> Enviar repostas? SIM [1], NÃO[2]: '))

                if op1 == 1:
                    enviando_resposta(lista_idQuestao, lista_alternativas, token, idProva)
                    op2 = int(input('\n> Deseja receber o resultado? SIM [1], NÃO[2]: '))
                    if op2 == 1:
                        r = requisicao_resultado(token, idProva)
                        print(r)
                    else:
                        break
                else:
                    break

            elif op == 2: 
                logout(token)
                auth = False
            else:
                print('> Opção inválida.')
