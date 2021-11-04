#importe as bibliotecas
import numpy as np
import sys
import sounddevice as sd
from suaBibSignal import signalMeu
import matplotlib.pyplot as plt
import peakutils


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
    
    #VALORES ACIMA DE 1 GERAM PICOS BEM MAIORES DO QUE O ESPERADO (VERIFICAR!!)
    duration = 10  #tempo em segundos que ira emitir o sinal acustico 
         
    gainX  = 0.3
    gainY  = 0.3


    print("Gerando Tons base")

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
    
    freq1 = freqs[numero][0]
    freq2 = freqs[numero][1]

    x1,senoide1 = signal.generateSin(freq1, amp, duration, fs)
    x2,senoide2 = signal.generateSin(freq2, amp, duration, fs)

    senoide = senoide1 + senoide2

    # reproduz o som
    sd.play(senoide, fs)
    # Exibe gráficos
    #plt.show()
    # aguarda fim do audio
    sd.wait()

    signal.plotSin(x1, numero, senoide)

    xf, yf = signal.calcFFT(senoide, fs)
    plt.figure("F(y)")
    plt.plot(xf,yf)
    plt.grid()
    plt.title('Fourier audio')
    plt.show()

    index = peakutils.indexes(yf ,thres = 0.5, min_dist=30)
    freq_picos = index/duration
    print("Picos identificados pela Transformada de Fourier: {} Hz e {} Hz".format(freq_picos[0],freq_picos[1]))


if __name__ == "__main__":
    main()
