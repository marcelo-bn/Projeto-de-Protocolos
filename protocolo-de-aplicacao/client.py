import mensagem_pb2
from socket import *

s = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
s.connect(('127.0.0.1', 9001))

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
def enviando_resposta(token, idProva):
    id_questao = [1,2]
    id_alternativas = [['v3p1'],['v4p1','v5p1']]

    # Questao 1 
    #cod1 = mensagem_pb2.CODIGOS()
    #cod1.codigos.append('v3p1')
    rsp1 = mensagem_pb2.RESPOSTA()
    rsp1.id = 1
    rsp1.codigos.codigos.append('v3p1')

    # Questao 2
    #cod2 = mensagem_pb2.CODIGOS()
    #cod2.codigos.append('v4p1')
    #cod2.codigos.append('v5p1')
    rsp2 = mensagem_pb2.RESPOSTA()
    rsp2.id = 2
    rsp2.codigos.codigos.append('v4p1')
    rsp2.codigos.codigos.append('v5p')

    # Mensagem REQ_RESP
    resposta_prova = mensagem_pb2.REQ_RESP()
    resposta_prova.token = token
    resposta_prova.id_prova = idProva
    resposta_prova.respostas.append(rsp1)
    resposta_prova.respostas.append(rsp2)

    msg = mensagem_pb2.MENSAGEM()
    msg.reqresp.token = resposta_prova.token
    msg.reqresp.id_prova = resposta_prova.id_prova 
    msg.reqresp.respostas.append(resposta_prova.respostas[0]) 
    msg.reqresp.respostas.append(resposta_prova.respostas[1]) 
    data = msg.SerializeToString()

    resposta = envia(data)

    return resposta

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

        while auth:
            op = -1
            print('> 1 - Iniciar prova.')
            print('> 2 - Sair da sua conta.')
            op = int(input('> O que você deseja? '))

            if op == 1:
                idProva = input('> Insira o id da prova fornecido pelo seu professor.')
                r = requisicao_prova(token, idProva)
                print("Prova: ")
                print(r.ackreqprova)

                op1 = int(input('> Enviar repostas? SIM [1], NÃO[2] '))
                if op1 == 1:
                    enviando_resposta(token, idProva)
                    op2 = int(input('> Deseja receber o resultado? SIM [1], NÃO[2] '))
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
