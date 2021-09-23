#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 

import sys
from typing import AsyncContextManager
from enlace import *
import time
import numpy as np
import random
import time
from datagram import *

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM3"                  # Windows(variacao de)

def timeout(com1):
    t0 = time.time()
    while com1.rx.getBufferLen() < 14:
        tn = time.time()
        elapsed_time = tn - t0
        if elapsed_time > 5:
            return True
    return False

image = "img/test_image.png"

eop = (2145369870).to_bytes(4, byteorder='big')

def main():
    try:
        com1 = enlace('COM3')
        
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        com1.fisica.flush()
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("Comunicação aberta com sucesso!\n")


        #HANDSHAKE (envia 14 bytes: 10 do head e 4 do eop)
        status_hs = (1).to_bytes(1, byteorder='big')
        zero = (0).to_bytes(3, byteorder='big')
        handshake_head = dg_head(status_hs, zero, zero, zero)
        dg_handshake = datagram(handshake_head, eop)

        print("ENVIANDO HANDSHAKE")  
        com1.sendData(dg_handshake)      

        print("Esperando resposta do servidor...\n")  
        expired = timeout(com1)

        while expired:
            print('EXPIRED!!')
            com1.rx.clearBuffer()
            resp_timeout = input("Servidor demorou mais de 5 segundos para responder. Tentar novamente? [S/N]\n")
            if resp_timeout == 'S' or resp_timeout == 's':
                print("ENVIANDO HANDSHAKE NOVAMENTE")
                com1.sendData(dg_handshake)
                expired = timeout(com1)
            else:
                print("Encerrando comunicação")
                com1.disable()
                sys.exit("O usuário encerrou a transmissão")
        
        hs_response, len_hs_response = com1.getData(14)
        
        expected_hs_head = dg_head((2).to_bytes(1, byteorder='big'), zero, zero, zero)
        expected_hs_response = datagram(expected_hs_head, eop)

        while hs_response != expected_hs_response:
            com1.rx.clearBuffer()
            resp_status_error = input("Servidor retornou algo errado! Reenviar pacote? [S/N]\n")
            if resp_status_error == 'S' or resp_status_error == 's':
                print("ENVIANDO HANDSHAKE NOVAMENTE")
                com1.sendData(dg_handshake)
                hs_response, len_hs_response = com1.getData(14)
            else:
                print("Encerrando comunicação")
                com1.disable()
                sys.exit("O usuário encerrou a transmissão")

        print("Handshake estabelecido com sucesso.\n")

        print("Iniciando a transmissão da imagem")
        txBuffer = open(image,'rb').read()

        #Para simular erros na comunicação, alterar False para True
        packages = dg_fragmentation(txBuffer, pckg_n_error=False, payload_error = False)

        for package in packages:
            com1.sendData(package)

            #Client espera por retorno do server para saber se o pacote chegou sem problemas
            server_response, len_server_response = com1.getData(14)
            server_response_status = server_response[:1]
            server_response_status_int = int.from_bytes(server_response_status, byteorder='big')
            
            while server_response_status_int == 3:
                com1.rx.clearBuffer()
                server_response_error = input("SERVIDOR RELATOU UM ERRO NO ENVIO DO PACOTE! REENVIAR? [S/N]\n")
                if server_response_error == 'S' or server_response_error == 's':
                    print("ENVIANDO PACOTE NOVAMENTE")
                    com1.sendData(package)
                    server_response, len_server_response = com1.getData(14)
                    server_response_status = server_response[:1]
                    server_response_status_int = int.from_bytes(server_response_status, byteorder='big') 
                else:
                    print("Encerrando comunicação")
                    com1.disable()
                    sys.exit("O usuário encerrou a transmissão")

            print('Pacote enviado com sucesso')

        print("Imagem enviada com sucesso")

        final_response, final_response_len = com1.getData(14)
        final_response_status = final_response[:1]
        final_response_status_int = int.from_bytes(final_response_status, byteorder='big')

        if final_response_status_int == 2:
            print('Servidor informou que a transmissão foi realizada com sucesso!')
        else:
            print("Servidor informou alguma falha na comunicação")

        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
