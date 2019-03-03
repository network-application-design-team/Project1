#!/usr/bin/env python3

"""
A simple echo client
"""
import sys
import socket
import pickle
from cryptography.fernet import Fernet as frt
import hashlib
import ClientKeys
from pygame import mixer

if len(sys.argv) != 7:
	print("Not enough argument in the commandline")
	sys.exit[1]
else:
	host = sys.argv[2]
	port = sys.argv[4]
	size = sys.argv[6]
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))
	checkpoint = 1
	print("[Checkpoint " + str(checkpoint).zfill(2) + "] Connection to " + str(host) + " on port " + str(port)) 
	checkpoint += 1
	while 1:
		print("[Checkpoint " + str(checkpoint).zfill(2) + "] Listening for QR codes from RPi Camera that contain questions")
		checkpoint += 1
		


		#delete after you get qrcode working		
		#s.send()
		#data = s.recv(size)
		#s.close()
		#print ('Received:', data)
		Question = b'What is today?'
		print("[Checkpoint " + str(checkpoint).zfill(2) + "] New Question: " + str(Question))
		checkpoint += 1
		key = frt.generate_key()
		f = frt(key)
		cipher = f.encrypt(Question)
		print("[Checkpoint " + str(checkpoint).zfill(2) + "] Encrypt: Generated Keys: " + str(key) + " | Cipher text: " + str(cipher))
		checkpoint += 1

		m = hashlib.md5()
		m.update(cipher)
		md5Sum = m.hexdigest()
		message = (key, cipher, md5Sum)
		
		pickledMessage = pickle.dumps(message)
		print("[Checkpoint " + str(checkpoint).zfill(2) + "] Sending data: " + str(pickledMessage))
		checkpoint += 1
		#Send Message
		s.send(pickledMessage)
        	#Recieve Message (pickledAnswer)
		
		pickledAnswer = s.recv(size)
		print("[Checkpoint " + str(checkpoint).zfill(2) + "] Received data: " + str(picledAnswer))
		checkpoint += 1
		encryptedAnswer = pickle.loads(pickledAnswer)
		answer = f.decrypt(encryptedAnswer[0])
		print("[Checkpoint " + str(checkpoint).zfill(2) + "] Decrypt: Using Key: " + str(key) + " | Plain text: " + str(answer))
		checkpoint += 1
		print("[Checkpoint " + str(checkpoint).zfill(2) + "] Speaking Answer: " + str(answer))
		checkpoint += 1
		text_to_speech = ClientKeys.returnTextToSpeech()
		with open('Answer.wav', 'wb') as audio_file:
			audio_file.write(
				text_to_speech.synthesize(
					str(answer),
					'audio/wav',
					'en-US_AllisonVoice'
				).get_result().content)

		mixer.init()
		mixer.music.load("Answer.wav")
		mixer.music.play()

