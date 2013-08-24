# -*- coding:utf-8 -*-
import pyaudio
import wave
import serial
import time
from irtoy import IrToy


def send_ir_code(codename="power-on"):
	s = serial.Serial(port='/dev/tty.usbmodem00000001', timeout=1)
	ir = IrToy(s)
	raw_packet['power-on'] = """01 92 00 C6 00 1E 00 4E 00 1E 00 1E 00 1E 00 1E  
	 00 1E 00 1E 00 1E 00 4E 00 1E 00 1E 00 1E 00 1E 
	 00 1E 00 1E 00 1E 00 1E 00 1E 00 1E 00 1E 00 1E 
	 00 1E 00 1E 00 1E 00 1E 00 1E 00 1E 00 1E 00 1E 
	 00 1E 00 1E 00 1E 00 1E 00 1E 00 1E 00 1E 00 4E 
	 00 1E 00 4E 00 1E 00 1E 00 1E 00 4E 00 1E 00 1E 
	 00 1E 00 1E 00 1E 00 1E 00 1E 00 4E 00 1E 00 4E 
	 00 1E 00 4E 00 1E FF FF                         """
	# on 18degree




	raw_packet['power-off'] = """01 92 00 C6 00 1E 00 4E 00 1E 00 1E 00 1E 00 1E  
	 00 1E 00 1E 00 1E 00 4E 00 1E 00 1E 00 1E 00 1E 
	 00 1E 00 1E 00 1E 00 4E 00 1E 00 4E 00 1E 00 1E 
	 00 1E 00 1E 00 1E 00 1E 00 1E 00 1E 00 1E       
	 00 1E 00 1E 00 1E 00 1E 00 1E 00 1E 00 1E 00 1E 
	 00 1E 00 1E 00 1E 00 1E 00 1E 00 1E 00 4E 00 1E 
	 00 1E 00 1E 00 4E 00 1E 00 1E 00 1E 00 1E 00 1E 
	 00 1E 00 1E 00 4E 00 1E FF FF                   """
	 # 끄기?

	raw_packet['mode-dry'] = """ 01 92 00 C6 00 1E 00 4E 00 1E 00 1E 00 1E 00 1E
	 00 1E 00 1E 00 1E 00 4E 00 1E 00 1E 00 1E 00 1E
	 00 1E 00 1E 00 1E 00 1E 00 1E 00 1E 00 1E 00 1E
	 00 1E 00 1E 00 1E 00 4E 00 1E 00 1E 00 1E      
	 00 1E 00 1E 00 4E 00 1E 00 4E 00 1E 00 1E 00 1E
	 00 1E 00 1E 00 1E 00 1E 00 1E 00 1E 00 1E 00 1E
	 00 1E 00 1E 00 1E 00 1E 00 1E 00 1E 00 1E 00 1E
	 00 1E 00 1E 00 4E 00 1E FF FF                  """
	# 모드2


	raw_packet = raw_packet[codename].replace(" ", "").replace("\n", "").decode('hex')
	raw_packet_l = [ord(c) for c in raw_packet]

	#name  LGE_6711A20015N
	bits=20
	#flags SPACE_ENC|CONST_LENGTH
	#eps            30
	# aeps          100

	# header 8576  4224 -> 8567us 
	# one           640  1664
	# zero          640   640
	# ptrail        640
	# pre_data_bits = 8
	pre_data = 0x88
	#actually this remote does not send any repeat signals!
	# gap = 1000000
	# toggle_bit      0

	# data = '00347'.encode('hex')

	# padding_length = bits - len(data) - 1

	# raw_data = pre_data +  + data

	try:
		# ir.reset()
		print "ir tr"
		ir.transmit(raw_packet_l)
		print "ir irmode"
		ir.IRMode()
		pass
	except Exception, e:
		pass
	print "ir reset"
	ir.reset()

## audio part
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 4
WAVE_OUTPUT_FILENAME = "output.wav"

frames = []

start_time = None

def callback(in_data, frame_count, time_info, status):
    global frames, start_time
    frames.append(in_data)
    if start_time == None:
    	start_time = time_info['current_time']

    # print "frame_count = ", frame_count , " time_info = " , time_info, " status = ", status
    # if (frame_count > 44100 * 2):
    if (time_info['current_time'] - start_time) > 2:
    	return (None, pyaudio.paAbort)
    else:
    	return (None, pyaudio.paContinue)


p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                # output=True,
                stream_callback=callback,
                frames_per_buffer=CHUNK)

print "about to start stream"
stream.start_stream()
print "stream started and about to ir"

## ir part start
send_ir_code('power-on')
## ir part end

print "ir end and waiting"

# for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
#     data = stream.read(CHUNK)
#     frames.append(data)


while stream.is_active():
	print "waiting for streaming"
	time.sleep(1)

print("* done recording")
	
stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()



"""
FFT Test code in python

Withrobot Lab.
http://withrobot.com
2008.4.28
"""
 
from pylab import *
from numpy.fft import fft, fftshift

Fs = 1000.          # the sampling frequency
Ts = 1./Fs          # the sampling period

N = 256             # 샘플 갯수
freqStep = Fs/N  # resolution of the frequency in frequency domain

f = 10*freqStep     # frequency of the wave 
t = arange(N)*Ts   # x ticks in time domain, t = n*Ts
y = cos(2*pi*f*t) + 0.5*sin(2*pi*3*f*t)  # 테스트 신호



Y = fft(y)          # FFT 분석
Y = fftshift(Y)    # middles the zero-point's axis
 
figure(figsize=(8,8))
subplots_adjust(hspace=.4)
 
# Plot time data
subplot(3,1,1)
plot(t, y, '.-')
grid("on")
xlabel('Time (seconds)')
ylabel('Amplitude')
title('signals')
axis('tight')
 
freq = freqStep * arange(-N/2, N/2)  # x ticks in frequency domain
 
# Plot spectral magnitude
subplot(3,1,2)
plot(freq, abs(Y), '.-b')
grid("on")
xlabel('Frequency')
ylabel('Magnitude (Linear)')
 
# Plot phase
subplot(3,1,3)
plot(freq, angle(Y), '.-b')
grid("on")
xlabel('Frequency')
ylabel('Phase (Radian)')
 
show()

