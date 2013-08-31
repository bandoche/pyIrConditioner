# coding=utf-8
import urllib, urllib2, base64, md5, cookielib
import sys
import json
import shutil
import subprocess


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
# --- phase 2: send ir code (skip)



# --- phase 3: conver audio
# convert audio to mp3
# copy file to rails folder
# convert_audio(command_idx, IRCON_FILE_UPLOAD_PATH)


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