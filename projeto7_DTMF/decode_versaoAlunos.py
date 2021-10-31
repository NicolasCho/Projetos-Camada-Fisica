#!/usr/bin/env python3
"""Show a text-mode spectrogram using live microphone data."""

#Importe todas as bibliotecas
from suaBibSignal import signalMeu
import peakutils
import matplotlib.pyplot as plt
import sounddevice as sd
import sys
import numpy as np
import time


#funcao para transformas intensidade acustica em dB
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)

def encontra_tecla(frequencias, f_dict):
    """
    Recebe as frequências de pico e devolve a tecla correspondente as frequências
    """
    matches = []
    freq_list = [697, 770, 852, 941, 1209, 1336, 1477]
    for i in frequencias:
        for j in freq_list:
            if i >= j-5 and i <= j+5:
                matches.append(j)
    print(matches)


    for numero, dupla_freq in f_dict.items():
        if matches == dupla_freq:
            tecla = numero
    return tecla

def main():

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

    signal = signalMeu()
    fs = 44100

    
    sd.default.samplerate = fs #taxa de amostragem
    sd.default.channels = 2  #voce pode ter que alterar isso dependendo da sua placa
    duration = 5 #tempo em segundos que ira aquisitar o sinal acustico captado pelo mic


    print("A gravação iniciará em 5 segundos!")
    for i in range (5, 0 ,-1):
        print(i)
        time.sleep(1)
    
    print("Gravação iniciada")
   
    numAmostras = fs * duration
   
    audio = sd.rec(int(numAmostras), fs, channels=2)  #NÃO ESTÁ GRAVANDO(?)!! VERIFICAR
    sd.wait()
    print("...     FIM")

    audio = audio[:,0]

    signal.plotAudio(audio, numAmostras, duration)   
    
    ## Calcula e exibe o Fourier do sinal audio. como saida tem-se a amplitude e as frequencias
    xf, yf = signal.calcFFT(audio, fs)
    plt.figure("F(y)")
    plt.plot(xf,yf)
    plt.grid()
    plt.title('Fourier audio')
    plt.show()
    

   
    index = peakutils.indexes(yf ,thres = 0.1, min_dist=30)
    f_picos = index/duration
    #print(yf[index]/5)
    
    #encontre na tabela duas frequencias proximas às frequencias de pico encontradas e descubra qual foi a tecla
    #print a tecla.
    tecla = encontra_tecla(f_picos, freqs)
    print("A tecla identificada foi:",tecla)
    ## Exibe gráficos
    #plt.show()

if __name__ == "__main__":
    main()
