#!/usr/bin/env python3

"""
A simple echo client
"""
# Imports for QR scanner
from __future__ import print_function
from picamera import PiCamera
from time import sleep
import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2

# Imports for rest of client
import signal
import sys
import socket
import pickle
from cryptography.fernet import Fernet as frt
import hashlib
import ClientKeys
from pygame import mixer
import datetime
#import netaddr 

def signal_handler(sig, frame):
    sys.exit(0)
    


if len(sys.argv) != 7:
	print("Not enough argument in the commandline")
	sys.exit[1]
else:
	host = sys.argv[2]
#	host = '172.30.111.201'		
#	host = int(netaddr.IPAddress(host))
#	print(host)
#	print(type(host))
	port = int(sys.argv[4])
	size = int(sys.argv[6])


	while 1:

		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((host,port))
		checkpoint = 1
		print("[" + str(datetime.datetime.now())  + "] [Checkpoint " + str(checkpoint).zfill(2) + "] Connection to " + str(host) + " on port " + str(port))

		checkpoint += 1
		print("[" + str(datetime.datetime.now())  + "] [Checkpoint " + str(checkpoint).zfill(2) + "] Listening for QR codes from RPi Camera that contain questions")
		checkpoint += 1
		
		while 1:
			signal.signal(signal.SIGINT, signal_handler)
			try:
                            # Start of code for QR scanner
                            # Initialize the camera and have it take a picture
				camera=PiCamera()
				camera.start_preview()
				sleep(2)
				camera.capture('/home/pi/projects/Project1/qr_image.jpg')
				camera.stop_preview()
				camera.close()
                            # Use cv2 library to find the QR code from the picture taken
				im=cv2.imread('/home/pi/projects/Project1/qr_image.jpg')
                            # Decode the found QR code
				decodedObject=pyzbar.decode(im)
				Question=decodedObject[0].data
				break;
			except:

				print("["+str(datetime.datetime.now())  + "] [Error, picture taken is not a QR code, Retrying now]")
 

		print("[" + str(datetime.datetime.now())  + "] [Checkpoint " + str(checkpoint).zfill(2) + "] New Question: " + str(Question,'utf-8'))
		checkpoint += 1
		key = frt.generate_key()
		f = frt(key)
		cipher = f.encrypt(Question)
		print("[" + str(datetime.datetime.now())  + "] [Checkpoint " + str(checkpoint).zfill(2) + "] Encrypt: Generated Keys: " + str(key) + " | Cipher text: " + str(cipher))
		checkpoint += 1

		m = hashlib.md5()
		m.update(cipher)
		md5Sum = m.hexdigest()
		message = (key, cipher, md5Sum)
	
		pickledMessage = pickle.dumps(message)
		print("[" + str(datetime.datetime.now())  + "] [Checkpoint " + str(checkpoint).zfill(2) + "] Sending data: " + str(pickledMessage))
		checkpoint += 1
		#Send Message
		s.send(pickledMessage)
        	#Recieve Message (pickledAnswer)
		
		pickledAnswer = s.recv(size)
		print("[" + str(datetime.datetime.now())  + "] [Checkpoint " + str(checkpoint).zfill(2) + "] Received data: " + str(pickledAnswer))
		checkpoint += 1
		encryptedAnswer = pickle.loads(pickledAnswer)
		answer = f.decrypt(encryptedAnswer[0])
		print("[" + str(datetime.datetime.now())  + "] [Checkpoint " + str(checkpoint).zfill(2) + "] Decrypt: Using Key: " + str(key) + " | Plain text: " + str(answer))
		checkpoint += 1
		print("[" + str(datetime.datetime.now())  + "] [Checkpoint " + str(checkpoint).zfill(2) + "] Speaking Answer: " + str(answer,'utf-8'))
		checkpoint += 1
		text_to_speech = ClientKeys.returnTextToSpeech()
		with open('Answer.mp3', 'wb') as audio_file:
			audio_file.write(
				text_to_speech.synthesize(
					str(answer,'utf-8'),
					'audio/mp3',
					'en-US_AllisonVoice'
				).get_result().content)
		mixer.init()
		mixer.music.load("Answer.mp3")
		mixer.music.play()
		while mixer.music.get_busy():
			sleep(1)
		s.close()



