import matplotlib
matplotlib.use('TkAgg') # THIS MAKES IT FAST!

import scipy
import wave
import struct
import numpy
import pylab

fp = wave.open('./output.wav', 'rb')

samplerate = fp.getframerate()
totalsamples = fp.getnframes()
fft_length = 512 # Guess
num_fft = (totalsamples / fft_length) - 2

#print (samplerate)
print "samplerate = %d, totalsamples = %d, fft_length = %d, num_fft = %d" % (samplerate, totalsamples, fft_length, num_fft)
print "fft_length = %d, fp.getnchannels() = %d / fp.getsampwidth() = %d" % (fft_length, fp.getnchannels(), fp.getsampwidth())
temp = numpy.zeros((num_fft, fft_length), float)

# leftchannel = numpy.zeros((num_fft, fft_length), float)
# rightchannel = numpy.zeros((num_fft, fft_length), float)

for i in range(num_fft):

	tempb = fp.readframes(fft_length / fp.getnchannels() / fp.getsampwidth());

	up = (struct.unpack("%dB"%(fft_length), tempb))

	X = numpy.array(up, float) - 128.0
	temp[i,:] = 20*scipy.log10(scipy.absolute(X))

for item in temp:
	for i in item:
		print "%f," % i,
	print


temp = temp * numpy.hamming(fft_length)
temp.shape = (-1, fp.getnchannels())
print temp

fftd = numpy.fft.fft(temp)
print fftd


f = scipy.linspace(0, fft_length, totalsamples - (fft_length * 2), endpoint=False)
# pylab.plot(f, Xdb)
print f
print len(f)
print fftd
print len(fftd[:,0])

pylab.plot(f, abs(fftd[:,0]))

pylab.show()




#########


"""
x, fs, nbits = audiolab.wavread('output.wav')
audiolab.play(x, fs)
N = 4*fs    # four seconds of audio
X = scipy.fft(x[:N])
Xdb = 20*scipy.log10(scipy.absolute(X))
f = scipy.linspace(0, fs, N, endpoint=False)
pylab.plot(f, Xdb)
pylab.xlim(0, 20000)   # view up to 5 kHz
H = scipy.fft(h)

Y = X*H
y = scipy.real(scipy.ifft(Y))
"""