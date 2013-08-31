# -*- coding:utf-8 -*-
import matplotlib
matplotlib.use('TkAgg') # THIS MAKES IT FAST!

import scipy
import wave
import struct
import numpy
import pylab
from mpl_toolkits.mplot3d.axes3d import Axes3D
import matplotlib.pyplot as plt
from pylab import *

fp = wave.open('./output.wav', 'rb')

samplerate = fp.getframerate() # 44100
totalsamples = fp.getnframes() # 90112
fft_length = 512 # Guess
num_fft = (totalsamples / fft_length) - 2

#print (samplerate)
print "samplerate = %d, totalsamples = %d, fft_length = %d, num_fft = %d" % (samplerate, totalsamples, fft_length, num_fft)
print "fft_length = %d, fp.getnchannels() = %d / fp.getsampwidth() = %d" % (fft_length, fp.getnchannels(), fp.getsampwidth())
temp = numpy.zeros((num_fft, fft_length), float)




# 1. 소리가 가장 작은 파트를 잡는다
# 2. 샘플링 해서 fft 값을 얻는다
# 3. 전체 fft[]에서 작은 부분 fft를 뺀다
# 4. ... 근데 이거 문제는 우연히 비프음 때 소리가 작으면 망ㅋ

# 다시
# 1. 평균을 낸다
# 2. 평균 값을 뺀다
# 3. (다른 소리에 비해 4khz가 특별히 오르는 경우를 파악하기 위해) 4hkz대와 아닌 곳의 차이를 계산
# 4. 근데 이거 뭐 계산 또 하려면 골치아프잖아... 그냥 4khz만 보고 특별히 증가가 있으면 있다고 할까....

# Fs = 44100;                    % Sampling frequency
# T = 1/Fs;                     % Sample time
# L = 512;                     % Length of signal
# t = (0:L-1)*T;                % Time vector
# NFFT = 2^nextpow2(L); % Next power of 2 from length of y
# Y = fft(data(1:512, 1) ,NFFT)/L;
# f = Fs/2*linspace(0,1,NFFT/2+1);

# plot(f,2*abs(Y(1:NFFT/2+1))) 


# leftchannel = numpy.zeros((num_fft, fft_length), float)
# rightchannel = numpy.zeros((num_fft, fft_length), float)
fftd = numpy.zeros((num_fft, fft_length/2), float)
full_fftd = numpy.zeros((num_fft, fft_length), float)
target = []
for i in range(num_fft):

	tempb = fp.readframes(fft_length / fp.getnchannels() / fp.getsampwidth());

	up = (struct.unpack("%dh"%(fft_length / 2), tempb))

	# X = numpy.array(up, float) - 128.0
	# temp[i,:] = 20*scipy.log10(scipy.absolute(X))
	full_fftd[i, :] = abs((numpy.fft.fft(up,fft_length)))
	fftd[i, :] = full_fftd[i, fft_length/2:]
	# print fftd[i, :]


	freqs = numpy.fft.fftfreq(fft_length)
	# print freqs[44:47] * samplerate
	target.append( float(numpy.abs(full_fftd[i, 43:49]).sum()) )

	idx=numpy.argmax(numpy.abs(full_fftd[i, :])**2)
	freq=freqs[idx] 
	freq_in_hertz=abs(freq*samplerate)
	# print(freq_in_hertz)

	# print fftd[i, :]
	# print len(fftd)

fft_avg = reduce(lambda x, y: x + y , fftd) / len(fftd)
fftd = fftd - fft_avg


fig = plt.figure(figsize=(17, 51))
phi_m = linspace(0, 17,174)
phi_p = linspace(0, 51,fft_length/2)
X,Y = meshgrid(phi_p, phi_m)
Z = fftd
# print fftd
print len(X)
print len(Y)
print len(Z)
print len(Z[0])
# sys.exit()

# make 2d plot
# pylab.plot(fft_avg)
# pylab.show()
# sys.exit()


# # make 3d plot
# `ax` is a 3D-aware axis instance, because of the projection='3d' keyword argument to add_subplot
ax = fig.add_subplot(1, 2, 1, projection='3d')

p = ax.plot_surface(X, Y, Z, rstride=4, cstride=4, linewidth=0)
show()
# surface_plot with color grading and color bar
# ax = fig.add_subplot(1, 2, 2, projection='3d')
# p = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)
# cb = fig.colorbar(p, shrink=0.5)


# for item in temp:
# 	for i in item:
# 		print "%f," % i,
# 	print


# temp = temp * numpy.hamming(fft_length)
# temp.shape = (-1, fp.getnchannels())
# print temp

# print fftd


# f = scipy.linspace(0, fft_length, totalsamples - (fft_length * 2), endpoint=False)
# # pylab.plot(f, Xdb)
# print f
# print len(f)
# print fftd
# print len(fftd[:,0])

# pylab.plot(f, abs(fftd[:,0]))

# pylab.show()




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