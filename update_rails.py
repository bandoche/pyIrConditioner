# coding=utf-8
import urllib, urllib2, base64, md5, cookielib
import sys
import json
import shutil
import subprocess

# irtoy part
import pyaudio
import wave
import serial
import time
from irtoy import IrToy

# irtoy part
# 2do - make raw code from data (how to code data to this raw data?)
def send_ir_code(codename="power-on"):
	raw_packet = {}
	s = serial.Serial(port='/dev/tty.usbmodem00000001', timeout=1)
	ir = IrToy(s)
	raw_packet['UN-JEON/JEONG-JI_18'] = """01 92 00 C6 00 1E 00 4E 00 1E 00 1E 00 1E 00 1E  
	 00 1E 00 1E 00 1E 00 4E 00 1E 00 1E 00 1E 00 1E 
	 00 1E 00 1E 00 1E 00 1E 00 1E 00 1E 00 1E 00 1E 
	 00 1E 00 1E 00 1E 00 1E 00 1E 00 1E 00 1E 00 1E 
	 00 1E 00 1E 00 1E 00 1E 00 1E 00 1E 00 1E 00 4E 
	 00 1E 00 4E 00 1E 00 1E 00 1E 00 4E 00 1E 00 1E 
	 00 1E 00 1E 00 1E 00 1E 00 1E 00 4E 00 1E 00 4E 
	 00 1E 00 4E 00 1E FF FF                         """
	# on 18degree




	raw_packet['UN-JEON/JEONG-JI_OFF'] = """01 92 00 C6 00 1E 00 4E 00 1E 00 1E 00 1E 00 1E  
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


	raw_packet = raw_packet[codename].replace(" ", "").replace("\n", "").replace("\t", "").decode('hex')
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


def rec_and_ir(format, channels, rate, chunk, ir_code_name, wave_filename):
	global frames
	p = pyaudio.PyAudio()
	stream = p.open(format=format,
	                channels=channels,
	                rate=rate,
	                input=True,
	                # output=True,
	                stream_callback=callback,
	                frames_per_buffer=chunk)

	print "about to start stream"
	stream.start_stream()
	print "stream started and about to ir"

	## ir part start
	#send_ir_code('power-on')
	send_ir_code(ir_code_name)
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

	wf = wave.open(wave_filename, 'wb')
	wf.setnchannels(channels)
	wf.setsampwidth(p.get_sample_size(format))
	wf.setframerate(rate)
	wf.writeframes(b''.join(frames))
	wf.close()


## audio part
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 4
WAVE_OUTPUT_FILENAME = "output.wav"

frames = []

start_time = None


# rails part
def convert_audio(command_idx, upload_path):
	wav = 'output'
	cmd = 'lame --preset insane %s.wav' % wav
	subprocess.call(cmd, shell=True)
	shutil.move(src=wav + '.mp3', dst=upload_path + 'audio/%s.mp3' % command_idx)


def debug(msg):
	with open('debug.log', 'a') as f:
		f.write(msg)


# credit @pablobm from http://stackoverflow.com/questions/4013838/urlencode-a-multidimensional-dictionary-in-python
def recursive_urlencode(d):
	def recursion(d, base=None):
		pairs = []

		for key, value in d.items():
			if hasattr(value, 'values'):
				pairs += recursion(value, key)
			else:
				new_pair = None
				if base:
					new_pair = "%s[%s]=%s" % (base, urllib.quote(unicode(key)), urllib.quote(unicode(value)))
				else:
					new_pair = "%s=%s" % (urllib.quote(unicode(key)), urllib.quote(unicode(value)))
				pairs.append(new_pair)
		return pairs

	return '&'.join(recursion(d))



IRCON_FILE_UPLOAD_PATH = '../../rails/IrConditioner/public/'
command_idx = sys.argv[1]

debug ('start %s' % command_idx)
# --- phase 1: get data

url = 'http://localhost:3000/commands/%s.json' % command_idx
req = urllib2.Request(url)
f = urllib2.urlopen(req)
data = f.read()
command = json.loads(data)

print command
# --- phase 2: send ir code
rec_and_ir(FORMAT, CHANNELS, RATE, CHUNK, command['button']['title'], WAVE_OUTPUT_FILENAME)

# --- phase 3: conver audio
# convert audio to mp3
# copy file to rails folder
convert_audio(command_idx, IRCON_FILE_UPLOAD_PATH)


# --- phase 4: update data to rails
command['audio_path'] = 'audio/%s.mp3' % command_idx
command['status'] = 2
command['button_id'] = int(command['button']['id'])
del(command['button'])

# urldata = urllib.urlencode({'command': command})
urldata = recursive_urlencode({'command': command})
request = urllib2.Request('http://localhost:3000/commands/%s.json' % command_idx, data=urldata)
request.get_method = lambda: 'PATCH'
resp = urllib2.urlopen(request)
print "resp: %s" % resp.read()