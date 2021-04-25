# Protocolo de Enlace
> Marcelo Bittencourt <br>
> Março de 2021


O protocolo de enlace a ser desenvolvido implementa um serviço com estas características:
* protocolo de enlace ponto-a-ponto para um canal sem-fio, e que usa uma camada física do tipo UART
* encapsulamento de mensagens com até 1024 bytes
* recepção de mensagens livres de erros
* garantia de entrega com mecanismo ARQ
* controle de acesso ao meio

