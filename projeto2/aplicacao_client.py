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
serialName = "COM3"                  # Windows(variacao de)

commands = [b'\x00\xFF', b'\x00', b'\x0F', b'\xF0', b'\xFF\x00', b'\xFF']
command_size = random.randint(10,15)
command_sequence = []
byte_msg = b''

for i in range(command_size):
    command = random.choice(commands)
    command_sequence.append(command)
    byte_msg += command + b'\x01'  #Adiciona b'\x01' para delimitar o comando
    

def numero_bytes(byte_list):
    n = 0
    for i in byte_list:
        n += len(i)
    return n

def main():
    try:
        com1 = enlace('COM3')
        
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        com1.fisica.flush()
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("Comunicação aberta com sucesso!\n")
        
        txBuffer = byte_msg
        n_commands = command_size
        txBuffer_len = len(txBuffer)

        print('COMANDOS A SEREM ENVIADOS:', command_sequence)
        print('NÚMERO DE COMANDOS: {} comandos'.format(n_commands))
        print('QUANTIDADE DE BYTES (ORIGINAL): {} bytes'.format(numero_bytes(command_sequence))) 
        print('MENSAGEM A SER ENVIADA (suja): {}'.format(byte_msg))
        print('QUANTIDADE DE BYTES DA MENSAGEM (SUJA): {} bytes\n'.format(txBuffer_len))
       
        print("Inicio da transmissão...")

        print("Enviando tamanho da mensagem")
        txBuffer_len_bytes = txBuffer_len.to_bytes(2,byteorder='big')
        #txBuffer_len_bytes = txBuffer_len.to_bytes(2,byteorder='big')    =>  len da lista em bytes

        t0 = time.time()
        com1.sendData(txBuffer_len_bytes)
        #com1.sendData(txBuffer_len_bytes)


        print("Enviando a mensagem (suja)\n")
        com1.sendData(txBuffer)


        print("Aguardando resposta do servidor...")

        #acesso aos bytes recebidos
        rxBuffer, nRx = com1.getData(2)
        tf = time.time()

        resposta_int = int.from_bytes(rxBuffer, byteorder='big')
        print("Resposta do sevidor: {} comandos!!" .format(resposta_int))

        if resposta_int == n_commands:
            print('Comunicação realizada com sucesso\n')
        else:
            print('Falha na comunicação, resposta do servidor divergente\n')

        delta_t = tf - t0
        print("TEMPO DE TRANSMISSÃO:", delta_t)

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
