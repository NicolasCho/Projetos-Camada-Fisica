#!/usr/bin/env python3
"""Show a text-mode spectrogram using live microphone data."""

#Importe todas as bibliotecas
from suaBibSignal import signalMeu
import peakutils
import matplotlib.pyplot as plt
import sounddevice as sd
import soundfile as sf
import sys
import numpy as np
import time


#funcao para transformas intensidade acustica em dB
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)

def main():
    signal = signalMeu()
    fs = 44100

    
    sd.default.samplerate = fs #taxa de amostragem
    sd.default.channels = 2  #voce pode ter que alterar isso dependendo da sua placa
    duration = 4 #tempo em segundos que ira aquisitar o sinal acustico captado pelo mic


    print("A gravação iniciará em 5 segundos!")
    for i in range (5, 0 ,-1):
        print(i)
        time.sleep(1)
    
    print("Gravação iniciada")
   
    numAmostras = fs * duration
   
    audio = sd.rec(int(numAmostras), fs, channels=2)  #NÃO ESTÁ GRAVANDO(?)!! VERIFICAR
    sd.wait()

    filename = 'audio.wav'
    sf.write(filename, audio, fs)

if __name__ == "__main__":
    main()
