from scipy.io.wavfile import read
from scipy.fftpack import fft, fftfreq
import numpy as np
import math

class AudioToMIDI():
	def __init__(self, audiofile, sample_rate=44100, fft_size=10000):
		a = read(audiofile)
		self.audio = np.array(a[1],dtype=float)
		self.fft_size = fft_size
		self.timestep = 1.0 / sample_rate
	def run_fft(self):
		n = []
		for i in range(self.fft_size, len(self.audio), self.fft_size):
			freqs = fft(self.audio[i-self.fft_size:i])[0:self.fft_size/2]
			xf = np.linspace(0.0, 1.0/(2.0*self.timestep), self.fft_size/2)
			n.append(np.vstack((xf, 2.0/self.fft_size * np.abs(freqs))).T)
		self.n = n
	def convert_midi(self):
		for fft_sample in self.n:
			for freq in fft_sample:
				note_freq = freq[0]
				note_amplitude = 2.0*self.timestep*freq[1]
				if note_amplitude > 0.3:
					print note_freq
					midi_note = 69 + (math.log(2, 12) * note_freq/440.0)
					print round(midi_note)

if __name__ == '__main__':
	a = AudioToMIDI("test.wav")
	a.run_fft()
	a.convert_midi()