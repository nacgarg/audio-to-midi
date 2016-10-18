from scipy.io.wavfile import read
from scipy.fftpack import fft
import numpy as np

class AudioToMIDI():
	def __init__(self, audiofile, sample_rate=44100, fft_size=600):
		a = read(audiofile)
		self.audio = np.array(a[1],dtype=float)
		self.timestep = 1.0 / sample_rate
	def run_fft():
		# run fft
		# set self.notes or something like that to a 2d array of notes happening at every timestep
	def convert_midi():
		# save self.notes as a midi