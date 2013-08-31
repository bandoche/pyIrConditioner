# -*- coding:utf-8 -*-
import pyaudio
import wave
import serial
import time
from irtoy import IrToy



# 2do - make raw code from data (how to code data to this raw data?)
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




