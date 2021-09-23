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
import time
from datagram import *

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM4"                  # Windows(variacao de)



def success():
    """
    Retorna um datagrama informando o cliente que a mensagem foi recebida com sucesso
    """
    eop = (2145369870).to_bytes(4, byteorder='big')
    status = (2).to_bytes(1, byteorder='big')
    zero = (0).to_bytes(3, byteorder='big')
    success_head = dg_head(status, zero, zero, zero)
    return datagram(success_head, eop)

def failure():
    """
    Retorna um datagrama informando o cliente que a mensagem NÃO foi recebida com sucesso (reenviar o pacote)
    """
    eop = (2145369870).to_bytes(4, byteorder='big')
    status = (3).to_bytes(1, byteorder='big')
    zero = (0).to_bytes(3, byteorder='big')
    failure_head = dg_head(status, zero, zero, zero)
    return datagram(failure_head, eop)

def main():
    try:
        com2 = enlace('COM4')
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com2.enable()

        com2.fisica.flush()
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("Comunicação aberta com sucesso!\n")

        print("Aguardando conexão..")
        com2.getData(14)        #Recebe 14 bytes do handshake

        print("Handshake recebido!")
        print("Reportando ao cliente\n")
        com2.sendData(success())
          
        print("Inicio da recepção da imagem")
        
        pckg_n_validator = 1
        eop_validator = (2145369870).to_bytes(4, byteorder='big')
        message = b''
        keep_alive = True

        while keep_alive:
            #Recebe primeiro o head (10 bytes fixo)
            head, len_head = com2.getData(10)  

            n_of_pckgs = head[1:4]
            n_of_pckgs_int = int.from_bytes(n_of_pckgs, byteorder='big')

            pckg_n = head[4:7]
            pckg_n_int = int.from_bytes(pckg_n, byteorder='big')

            payload_size = head[7:]
            payload_size_int = int.from_bytes(payload_size, byteorder='big')

            #Sabendo o tamanho do payload, recebe-se o mesmo
            payload, len_payload = com2.getData(payload_size_int)

            #Por fim, recebe-se o EOP
            eop, len_eop = com2.getData(4)


            #Verificar número do pacote e eop
            if pckg_n_int != pckg_n_validator:
                com2.rx.clearBuffer()
                print("NÚMERO DO PACOTE ERRADO\n")
                print("Número esperado: {} /// Número recebido: {}".format(pckg_n_validator, pckg_n_int))
                print("Solicitando reenvio do pacote...")
                com2.sendData(failure())
            
            
            elif eop != eop_validator:
                com2.rx.clearBuffer()
                print("EOP ERRADO OU FORA DE LUGAR (TAMANHO DO PAYLOAD DIVERGENTE AO INFORMADO NO HEAD)\n")
                print("Solicitando reenvio do pacote...")
                com2.sendData(failure())
            
            else:
                print('pacote {} recebido com sucesso'.format(pckg_n_int))
                com2.sendData(success())
                message += payload
                pckg_n_validator += 1
            
            
            
            if pckg_n_int == n_of_pckgs_int:
                print('Todos os pacotes foram recebidos')
                keep_alive = False
                
        #Salvando a imagem recebida
        imageW = "img/test_image_clone.png"
        f = open(imageW,"wb")
        f.write(message)

        print("Imagem salva!")

        com2.sendData(success())
        
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