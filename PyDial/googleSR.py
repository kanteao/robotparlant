#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import speech_recognition as sr
import wave
from ast import literal_eval

def speechRecognition(data, params):
	r = sr.Recognizer()

	audioFileName = 'test.wav'
	data = base64.b64decode(data)
	params = base64.b64decode(params)
	params = literal_eval(params)

	wave_write = wave.open(audioFileName,"w") 
	wave_write.setparams(params)
	wave_write.writeframes(data)
	wave_write.close()

	audioFile = None
	with sr.AudioFile(audioFileName) as source:
		audioFile = r.record(source)

	try:
		text = r.recognize_google(audioFile, language="en-EN")
		return text
		
	except Exception as e:
		print (e)
