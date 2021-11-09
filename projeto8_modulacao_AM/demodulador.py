from suaBibSignal import *
import peakutils
import matplotlib.pyplot as plt
import sounddevice as sd
import soundfile as sf
import sys
import numpy as np
import time
from scipy.io.wavfile import read
from funcoes_LPF import *


signal = signalMeu()
audio, fs = sf.read('audios/am_audio.wav')
duration = 4
samples = fs*duration

#Áudio recebido
signal.plotAudio(audio, samples, duration,'Áudio modulado no domínio do tempo')   
signal.plotFFT(audio, fs, 'Áudio modulado no domínio da frequência (Fourier)')

# Demodulador
carrier = signal.generateSin(14000, 1, duration, fs)[1]
audio_demo = audio * carrier
signal.plotAudio(audio_demo, samples, duration,'Áudio demodulado no domínio do tempo')   
# Gráfico 6 - Sinal de áudio demodulado no domínio da frequência
signal.plotFFT(audio_demo, fs, 'Áudio demodulado no domínio da frequência (Fourier)')
sd.play(audio_demo, fs) 
sd.wait()

#Filtro
audio_filtered = filtro(audio_demo, fs, 4000)
signal.plotAudio(audio_filtered, samples, duration,'Áudio demodulado e filtrado no domínio do tempo')  
# Gráfico 7 - Sinal de áudio demodulado e filtrado no domínio da frequência
signal.plotFFT(audio_filtered, fs, 'Áudio demodulado e filtrado no domínio da frequência (Fourier)')
sd.play(audio_filtered, fs) 
sd.wait()


#filename = 'audios/audio_demodulado.wav'
#sf.write(filename, audio_filtered, fs)