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

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM5"                  # Windows(variacao de)

def main():
    try:
        com2 = enlace('COM5')
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com2.enable()

        com2.fisica.flush()
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("Comunicação aberta com sucesso!\n")
    
          
        print("Inicio da recepção...")
        #txBuffer = dados


        print("Aguardando tamanho da mensagem(suja)")

        rxBuffer_len, size = com2.getData(2)       
        rxBuffer_len_int = int.from_bytes(rxBuffer_len, byteorder='big')

        print("Tamanho da mensagem(suja): {} bytes\n".format(rxBuffer_len_int))

        print("Recebendo comandos")
        rxBuffer, nRx = com2.getData(rxBuffer_len_int)
        print("Comandos recebidos!\n")

        #Necessario separar e retirar os b'\x01' da mensagem para
        #descobrir o número de comandos

        message = rxBuffer.split(b'\x01')[:-1]
        n_commands = len(message)


        print("Enviando resposta para o Client\n")
        com2.sendData(n_commands.to_bytes(2, byteorder='big'))

        print("COMANDOS RECEBIDOS:", message)
        print("Número de comandos: {} comandos".format(n_commands))
    
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