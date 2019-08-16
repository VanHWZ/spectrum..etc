import numpy as np
import pyaudio
from scipy import signal
from scipy.io.wavfile import write

T = 5
samplingRate = 44100
freq = 440
samplesPerSec = np.arange(samplingRate*T)
carrier = np.sin(2*np.pi*samplesPerSec*freq/samplingRate)

amp1 = 0.3
amp2 = 1
sound = np.int16(carrier * 32767 * amp1) * amp2

write("%dhz.wav"%freq, samplingRate, sound)
