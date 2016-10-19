from scipy.io.wavfile import read
from scipy.fftpack import fft, fftfreq
import numpy as np
from mido import MidiFile, MidiTrack, Message
import math

class AudioToMIDI():
	def __init__(self, audiofile, sample_rate=44100, fft_size=1000):
		a = read(audiofile)
		if len(a[1].shape) > 1:
			a = (a[0], (a[1][:,1] + a[1][:,0])/2) # convert to mono
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
		mid = MidiFile()
		track = MidiTrack()
		mid.tracks.append(track)
		curr_on = []
		for fft_sample in self.n:
			for i, note in enumerate(curr_on):
				if i == 0:
					track.append(Message('note_off', note=note, velocity=0, time=100))
				else:
					track.append(Message('note_off', note=note, velocity=0, time=0))
			curr_on = []
			for freq in fft_sample:
				note_freq = freq[0]
				note_amplitude = 2.0*self.timestep*freq[1]

				if note_amplitude > 0.01 and note_freq > 10:
					midi_note = 69 + (math.log(note_freq/440.0, 2) * 12)
					midi_note = int(midi_note)
					if midi_note > 5:
						curr_on.append(midi_note)
						track.append(Message('note_on', note=midi_note, velocity=int(np.abs(note_amplitude)*80.0), time=0))
		mid.save('output.mid')
if __name__ == '__main__':
	a = AudioToMIDI("file.wav", 15000)
	a.run_fft()
	a.convert_midi()