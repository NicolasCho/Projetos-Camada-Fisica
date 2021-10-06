#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from enlace import *
import time
import numpy as np
import random
from datagram import *
import sys
from log import *

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM4"                  # Windows(variacao de)



def success(last_pckg):
    """
    Retorna um datagrama informando o cliente que a mensagem foi recebida com sucesso
    """
    eop = (2145369870).to_bytes(4, byteorder='big')
    success_head = dg_head(msg_type=4, last_pckg=last_pckg)
    return datagram(success_head, eop)

def failure(expected_pckg_no):
    """
    Retorna um datagrama informando o cliente que a mensagem NÃO foi recebida com sucesso (reenviar o pacote)
    """
    eop = (2145369870).to_bytes(4, byteorder='big')
    failure_head = dg_head(msg_type=6, expected_pckg=expected_pckg_no)
    return datagram(failure_head, eop)

def timeout_get(com2, msg_len, time_limit):
    t0 = time.time()
    while com2.rx.getBufferLen() < msg_len:
        tn = time.time()
        elapsed_time = tn - t0
        if elapsed_time > time_limit:
            return True, (0).to_bytes(1, byteorder='big')
    data, data_len = com2.getData(msg_len)
    return False, data

def comm_end():
    eop = (2145369870).to_bytes(4, byteorder='big')
    end_head = dg_head(msg_type=5)
    end_dg = datagram(end_head, eop)
    return end_dg

def hs_response():
    eop = (2145369870).to_bytes(4, byteorder='big')
    hs_response_head = dg_head(msg_type=2)
    hs_resp_dg = datagram(hs_response_head, eop)  
    return hs_resp_dg

HS_ERROR = False
TIMEOUT_ERROR = False

def main():
    try:
        # ID DO SERVER: 2
        com2 = enlace('COM4')
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com2.enable()

        com2.fisica.flush()
        
        print("Comunicação aberta com sucesso!\n")

        #TRANSMISSION STATUS
        ts_list = []
        log = ''

        print("Aguardando conexão..")

        ocioso = True
        run = True

        while run:
            timer_hs = time.time()
            if HS_ERROR:                            ####### Para simular erro no tempo de resposta do handshake, mudar HS_ERROR para True #############
                time.sleep(25)
            while ocioso:
                com2.rx.clearBuffer()
                timer_hs_f = time.time()
                if timer_hs_f - timer_hs > 20:
                    if 3 not in ts_list:                                                #ADICIONA 3 A LISTA DE OCORRENCIAS NA TRANSMISSÃO
                        ts_list.append(3)
                    print('TENTATIVA DE COMUNICAÇÃO ULTRAPASSOU 20 SEGUNDOS!')

                print('ocioso')
                nao_recebeu, hs = timeout_get(com2, 14, 1)
                
                if not nao_recebeu and hs[0] == 1:
                    if hs[2] == 2:
                        n_of_pckgs = hs[3]
                        ocioso = False

            log += write_line(1, 'receb', 14)

            print('Servidor recebeu handshake!')
            com2.sendData(hs_response())                #mensagem do tipo 2
            log += write_line(2, 'envio', 14)
            print('Preparando para receber pacotes...\n')

            message = b''
            expected_pckg_no = 1
            expected_eop = (2145369870).to_bytes(4, byteorder='big')
            com2.rx.clearBuffer()

            while expected_pckg_no <= n_of_pckgs:
                timer2 = time.time()
                next = False

                while not next:
                    expired, package_received = timeout_get(com2, 10, 2) #Receber head do pacote

                    if package_received[0] == 3 and not TIMEOUT_ERROR:
                        pckg_no = package_received[4]
                        payload_size = package_received[5]

                        payload, len_payload = com2.getData(payload_size)
                        
                        eop, len_eop = com2.getData(4)

                        log += write_line(3,'receb', len(package_received), pckg_n=pckg_no, n_of_pckgs=n_of_pckgs)
                        if pckg_no == expected_pckg_no and eop == expected_eop:
                            print('Pacote com payload e número correto')
                            message += payload
                            com2.sendData(success(pckg_no))          #mensagem do tipo 4
                            log += write_line(4, 'envio', 14)
                            expected_pckg_no += 1
                        else:
                            print('Pacote com algum erro no número ou payload!')
                            if 2 not in ts_list:                                        #ADICIONA 2 A LISTA DE OCORRENCIAS NA TRANSMISSÃO
                                ts_list.append(2)
                            com2.sendData(failure(expected_pckg_no))  #mensagem do tipo 6
                            log += write_line(6, 'envio', 14)
                        next = True

                    else:
                        if TIMEOUT_ERROR:                          ####### Para simular erro de timeout (>20), mudar HS_ERROR para True #############
                            time.sleep(25)
                        timer2_f = time.time()

                        if timer2_f - timer2 > 20:
                            if 4 not in ts_list:                                        #ADICIONA 4 A LISTA DE OCORRENCIAS NA TRANSMISSÃO
                                ts_list.append(4)
                            com2.sendData(comm_end)             #mensagem do tipo 5
                            log += write_line(5, 'envio', 14)
                            server_write_on_file(ts_list, log)
                            log = ''
                            print('Tentativa de comunicação ultrapassou 20 segundos!')
                            print('Encerrando comunicação')
                            ocioso = True
                            next = True
                            expected_pckg_no = 10000000
                        if expired:
                            print('Pacote demorou!')
                            if 5 not in ts_list:                                        #ADICIONA 5 A LISTA DE OCORRENCIAS NA TRANSMISSÃO
                                ts_list.append(5)
                            com2.rx.clearBuffer()
                            com2.sendData(failure(expected_pckg_no))        #mensagem do tipo 6
                            log += write_line(6, 'envio', 14)
                            print("mensagem de erro enviada")
                        
                if expected_pckg_no == n_of_pckgs+1:
                    run = False
                
        imageW = "img/test_image_clone.png"
        f = open(imageW,"wb")
        f.write(message)

        print("Imagem salva!")      

        server_write_on_file(ts_list, log)
        
        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com2.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com2.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()