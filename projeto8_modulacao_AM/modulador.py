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

#https://stackoverflow.com/questions/16778878/python-write-a-wav-file-into-numpy-float-array
signal = signalMeu()
wav_file = read("audios/audio.wav")
audio_array = np.array(wav_file[1],dtype=float)
audio_array = audio_array[:,0]
duration = 4
fs = 44100
samples = fs*duration

# Áudio original
signal.plotAudio(audio_array, samples, duration,'Áudio original no domínio do tempo')
signal.plotFFT(audio_array, fs, 'Áudio original no domínio da frequência (Fourier)')
#sd.play(audio_array, fs)  # Audio estourado!!
#sd.wait()

# Normalização no intervalo [-1,1]
max_value = np.max(np.abs(audio_array))
norm_const = 1/max_value
audio_norm = norm_const*audio_array
# GRÁFICO 1-Sinal do áudio original normalizado no domínio do tempo
signal.plotAudio(audio_norm, samples, duration,'Áudio normalizado no domínio do tempo')   
#sd.play(audio_norm, fs)  # Áudio normal
#sd.wait()
signal.plotFFT(audio_norm, fs, 'Áudio normalizado no domínio da frequência (Fourier)')

# Áudio filtrado
audio_filtered = filtro(audio_norm, fs, 4000)   # Função demora um pouco
# GRÁFICO 2 - Sinal de áudio filtrado no domínio do tempo 
signal.plotAudio(audio_filtered, samples, duration,'Áudio filtrado no domínio do tempo')   
# GRÁFICOS 3 - sinal de áudio filtrado no domínio da frequência
signal.plotFFT(audio_filtered, fs, 'Áudio filtrado no domínio da frequência (Fourier)')
sd.play(audio_filtered, fs)  # Áudio com baixa qualidade
sd.wait()

# Modulação 
carrier = signal.generateSin(14000, 1, duration, fs)[1]
audio_am = audio_filtered*carrier
# GRÁFICO 4 - Sinal de áudio modulado no domínio do tempo 
signal.plotAudio(audio_am, samples, duration,'Áudio modulado no domínio do tempo')   
# GRÁFICOS 5 - sinal de áudio modulado no domínio da frequência
signal.plotFFT(audio_am, fs, 'Áudio modulado no domínio da frequência (Fourier)')
sd.play(audio_am, fs)  # Não audível
sd.wait()

#Salva audio modulado:
#filename = 'audios/am_audio.wav'
#sf.write(filename, audio_am, fs)
