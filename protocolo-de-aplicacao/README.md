# Protocolo de Aplicação
> Marcelo Bittencourt <br>
> Abril de 2021

Protocolo de aplicação para um cenário de realização de provas *online*. As mensagens do protocolo
são baseados no padrão Protocol Buffers e possui as seguintes estruturas:

```
message LOGIN {
        required string login = 1;
        required string senha = 2;
} 
```
```
message ACK_LOGIN {
  optional string token = 1;
  required STATUS status = 2;
}
```
```
message STATUS {
  required int32 codigo = 1;
  optional string descricao = 2;
}
```
```
message REQ_PROVA {
  required string token = 1;
  optional string id_prova = 2;
}
```
```
message Alternativa {
  required string descricao = 1;
  required string codigo = 2;
}

message QUESTAO {
  required int32 id = 1;
  required string enunciado = 2;
  optional int32 pontos = 3;
  repeated Alternativa alternativas = 4;
}

message ACK_REQ_PROVA {
  required string id_prova = 1;
  repeated QUESTAO questoes = 2;
}
```
```
message CODIGOS {
    repeated string codigos = 1;
}

message RESPOSTA {
  required int32 id = 1;
  oneof resp {
    string texto = 2;
    CODIGOS codigos = 3;
  }
}

message REQ_RESP {
  required string token = 1;
  required string id_prova = 2;
  repeated RESPOSTA respostas = 3;
}
```
```
message REQ_RESULTADO {
  required string token = 1;
  required string id_prova = 2;
}
```
```
message RESULTADO {
  required int32 questao = 1;
  required int32 pontos = 2;
}

message ACK_REQ_RESULTADO {
  required string id_prova = 1;
  required int32 nota = 2;
  repeated RESULTADO questoes = 3;
}
```
```
message LOGOUT {
  required string token = 1;
}
```
```
message MENSAGEM {
  oneof msg {
    LOGIN login = 1;
    LOGOUT logout = 2;
    ACK_LOGIN acklogin = 3;
    STATUS status = 4;
    REQ_PROVA reqprova = 5;
    ACK_REQ_PROVA ackreqprova = 6;
    REQ_RESULTADO reqresultado = 7;
    ACK_REQ_RESULTADO ackreqresultado = 8;
    REQ_RESP reqresp = 9;
  }
}
```

## Compilando o projeto

Para simular as trocas das mensagens deve-se executar os programas *server.py* e *client.py*. Iniciei os testes sempre com o servidor já ativo.

```
python3 server.py 9000
```