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
from log import *
# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM3"                  # Windows(variacao de)

def timeout_get(com1, msg_len, time_limit):
    t0 = time.time()
    while com1.rx.getBufferLen() < msg_len:
        tn = time.time()
        elapsed_time = tn - t0
        if elapsed_time > time_limit:
            return True, (0).to_bytes(1, byteorder='big')
    data, data_len = com1.getData(msg_len)
    return False, data

def handshake(n_of_packages):
    """
        Cria handshake 
    """
    eop = (2145369870).to_bytes(4, byteorder='big')
    hs_head = dg_head(msg_type=1, n_of_pckgs=n_of_packages, archive_id=1)
    hs_dg = datagram(hs_head, eop)
    return hs_dg

def comm_end():
    eop = (2145369870).to_bytes(4, byteorder='big')
    end_head = dg_head(msg_type=5)
    end_dg = datagram(end_head, eop)
    return end_dg

image = "img/test_image.png"
eop = (2145369870).to_bytes(4, byteorder='big')
ERRO_DE_PACOTE = False

def main():
    try:
        com1 = enlace('COM3')
        
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        com1.fisica.flush()
        
        print("Comunicação aberta com sucesso!\n")

        #TRANSMISSION STATUS
        ts_list = []
        log = ''

        txBuffer = open(image,'rb').read()
        n_of_packages= get_n_of_pckgs(txBuffer)


        #HANDSHAKE (envia 14 bytes: 10 do head e 4 do eop)
        print("ENVIANDO HANDSHAKE")
        hs = handshake(n_of_packages)  
        com1.sendData(np.asarray(hs))  

        log += write_line(1, 'envio', 14)  

        timer_hs = time.time()

        print("Esperando resposta do servidor...\n")  
        expired, hs_response = timeout_get(com1, 14, 5)

        while expired or hs_response[0] != 2:
            timer_hs_f = time.time()
            if timer_hs_f - timer_hs > 20:
                if 3 not in ts_list:                                                    #ADICIONA 3 A LISTA DE OCORRENCIAS NA TRANSMISSÃO
                    ts_list.append(3)
                print('TENTATIVA DE COMUNICAÇÃO ULTRAPASSOU 20 SEGUNDOS!')

            com1.rx.clearBuffer()
            print('Servidor não retornou uma resposta dentro de 5 segundos ou retornou algo errado!')
            print("REENVIANDO HANDSHAKE")
            com1.sendData(np.asarray(hs)) 

            log += write_line(1, 'envio', 14) 

            expired, hs_response = timeout_get(com1, 14, 5)

        log += write_line(2, 'receb', 14)

        print("Handshake estabelecido com sucesso.\n")
        print("Iniciando a transmissão da imagem")
        pckg_no = 1

        while pckg_no <= n_of_packages:
            package = create_pckg(txBuffer, pckg_no, n_of_packages)

            if pckg_no == 6 and ERRO_DE_PACOTE:             ####### Para simular erro de ordem de pacote, mudar variável ERRO_DE_PACOTE para True. Numera o pacote 6 como 5  ###############
                package = create_pckg(txBuffer, pckg_no, n_of_packages, error=True)

            com1.sendData(package)

            log += write_line(3, 'envio', len(package), pckg_n = pckg_no, n_of_pckgs=n_of_packages)

            timer2 = time.time()        #timer de timeout
            expired, package_response = timeout_get(com1, 14, 5)

            if package_response[0] == 4:
                log += write_line(4, 'receb', len(package_response))
                print('Pacote recebido com sucesso pelo servidor')

            else:
                error = True
                while error:
                    if expired:
                        if 5 not in ts_list:                                                    #ADICIONA 5 A LISTA DE OCORRENCIAS NA TRANSMISSÃO
                            ts_list.append(5)
                        com1.rx.clearBuffer()
                        print("Servidor demorou mais de 5 segundos para responder!")
                        print("Reenviando pacote")
                        com1.sendData(package)

                        log += write_line(3, 'envio', len(package), pckg_n = pckg_no, n_of_pckgs=n_of_packages)

                        expired, package_response = timeout_get(com1, 14, 5)
                        
                    timer2_f = time.time()
                    if timer2_f - timer2 > 20:
                        if 4 not in ts_list:                                                    #ADICIONA 4 A LISTA DE OCORRENCIAS NA TRANSMISSÃO
                            ts_list.append(4)
                        com1.sendData(comm_end)

                        log += write_line(5,'envio', 14)
                        client_write_on_file(ts_list, log)
                        
                        print('Tentativa de comunicação ultrapassou 20 segundos!')
                        print('Encerrando comunicação')
                        com1.disable()
                        sys.exit("O cliente encerrou a transmissão")
                
                    if package_response[0] == 6:
                        log += write_line(6, 'receb', len(package_response))
                        if 2 not in ts_list:                                                    #ADICIONA 2 A LISTA DE OCORRENCIAS NA TRANSMISSÃO
                            ts_list.append(2)
                        print('Servidor recebeu pacote com número ou eop errados!')
                        com1.rx.clearBuffer()
                        pckg_no = package_response[6]
                        package = create_pckg(txBuffer, pckg_no, n_of_packages)
                        com1.sendData(package)

                        log += write_line(3, 'envio', len(package), pckg_n = pckg_no, n_of_pckgs=n_of_packages)

                        timer2 = time.time()
                        expired, package_response = timeout_get(com1, 14, 5)
                        
                    if package_response[0] == 4:
                        log += write_line(4, 'receb', len(package_response))
                        error = False
                        print('Pacote recebido com sucesso pelo servidor')
            
            pckg_no +=1

        print("Imagem enviada com sucesso")

        client_write_on_file(ts_list, log)

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
