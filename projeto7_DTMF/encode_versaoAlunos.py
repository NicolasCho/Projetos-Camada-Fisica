

#importe as bibliotecas
from suaBibSignal import signalMeu
import matplotlib.pyplot as plt
import sounddevice as sd
import sys
import numpy as np


def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

#converte intensidade em Db, caso queiram ...
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)

def getFrequencies(n):
    return None

def main():
    print("Inicializando encoder")
    
     #declare um objeto da classe da sua biblioteca de apoio (cedida)    
    #declare uma variavel com a frequencia de amostragem, sendo 44100

    signal = signalMeu()
    fs = 44100
    amp = 1

    
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:
    
    
    duration = 3  #tempo em segundos que ira emitir o sinal acustico 
      
#relativo ao volume. Um ganho alto pode saturar sua placa... comece com .3    
    gainX  = 0.3
    gainY  = 0.3


    print("Gerando Tons base")
    
    #gere duas senoides para cada frequencia da tabela DTMF ! Canal x e canal y 
    #use para isso sua biblioteca (cedida)
    #obtenha o vetor tempo tb.
    #deixe tudo como array

    freqs = {}
    freqs[0] = [941, 1336]
    freqs[1] = [697, 1209]
    freqs[2] = [697, 1336]
    freqs[3] = [697, 1477]
    freqs[4] = [770, 1209]
    freqs[5] = [770, 1336]
    freqs[6] = [770, 1477]
    freqs[7] = [852, 1209]
    freqs[8] = [852, 1336]
    freqs[9] = [852, 1477]

    #printe a mensagem para o usuario teclar um numero de 0 a 9. 
    #nao aceite outro valor de entrada.
    while True:    
        try:
            numero = int(input("Gerando Tom referente ao símbolo: "))
        except ValueError:
            print("Apenas valores inteiros!\n")
        else:
            if numero < 0 or numero > 9:
                print('Digitar número inteiro de 0 a 9!\n')
            else:
                break
    
    #construa o sunal a ser reproduzido. nao se esqueca de que é a soma das senoides
    freq1 = freqs[numero][0]
    freq2 = freqs[numero][1]

    senoide1 = signal.generateSin(freq1, amp, duration, fs)[1]
    senoide2 = signal.generateSin(freq2, amp, duration, fs)[1]

    senoide = senoide1 + senoide2

    #printe o grafico no tempo do sinal a ser reproduzido
    signal.plotSin(numero, senoide, fs, duration)
    signal.plotFFT(senoide, fs)


    # reproduz o som
    sd.play(senoide, fs)
    # Exibe gráficos
    #plt.show()
    # aguarda fim do audio
    sd.wait()

if __name__ == "__main__":
    main()
