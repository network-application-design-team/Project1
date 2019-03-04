
import socket
import sys
import wolframalpha
from cryptography.fernet import Fernet
import ServerKeys 
import pickle
import watson_developer_cloud
import datetime
import json
import time

from pygame import mixer
import hashlib

def fetch_ip():
      return((([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close())\
        for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0])

wolfClient = ServerKeys.returnAPI()

if len(sys.argv) != 5:
    	print("There was not enough arguments in the command line")
    	sys.exit[1]
else:
	
	checkpoint = 1
	host = fetch_ip()
#	print(host)
#	print(type(host))
	port = int(sys.argv[2])
	backlog = 5
	size = int(sys.argv[4])
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((host,port))
	s.listen(backlog)
	print("[" + str(datetime.datetime.now())  + "] [Checkpoint " + str(checkpoint).zfill(2) + "] Created socket at " + str(host) + " on port " + str(port))
	checkpoint += 1
	print("[" + str(datetime.datetime.now())  + "] [Checkpoint " + str(checkpoint).zfill(2) + "] Listening for client connections")
	checkpoint += 1
	while 1:

		client, address = s.accept()
		print("[" + str(datetime.datetime.now())  + "] [Checkpoint " + str(checkpoint).zfill(2) + "] Accepted client connection from  " + str(address) + " on port " + str(port))
		checkpoint += 1
		data = client.recv(size)
		print("[" + str(datetime.datetime.now())  + "] [Checkpoint " + str(checkpoint).zfill(2) + "] Received data:  " + str(data))
		checkpoint += 1
		unpickled = pickle.loads(data)
		key = unpickled[0]
		question = unpickled[1]
		md5hash = unpickled[2]
		f = Fernet(key)
		actQuestion = f.decrypt(question)

		
		strQuestion = str(actQuestion, 'utf-8')
		print("[" + str(datetime.datetime.now())  + "] [Checkpoint " + str(checkpoint).zfill(2) + "] Decrypt: Key: " + str(key) + " | Plain text: " + strQuestion)		
		checkpoint += 1
		print("[" + str(datetime.datetime.now())  + "] [Checkpoint " + str(checkpoint).zfill(2) + "] Speaking Question: " + strQuestion)
		checkpoint += 1

		text_to_speech = ServerKeys.returnTextToSpeech()
		with open('Question.mp3', 'wb') as audio_file:
			audio_file.write(
				text_to_speech.synthesize(
					str(strQuestion),
					'audio/mp3',
					'en-US_AllisonVoice'
				).get_result().content)
                
		mixer.init()
		mixer.music.load("Question.mp3")
		mixer.music.play()
	
		while mixer.music.get_busy():
			time.sleep(1)
		print("[" + str(datetime.datetime.now())  + "] [Checkpoint " + str(checkpoint).zfill(2) + "] Sending question to Wolframalpha " + strQuestion)

		checkpoint += 1
		wolframResponse = wolfClient.query(strQuestion)
		stringResponse = next(wolframResponse.results).text
		response = bytes(stringResponse, 'utf-8')
		print("[" + str(datetime.datetime.now())  + "] [Checkpoint " + str(checkpoint).zfill(2) + "] Received question from Wolframalpha " + str(stringResponse)) 
		checkpoint += 1
#		print(str(type(stringResponse)) + "Response: " + str(stringResponse))
		
		
	

		encryptedResponse = f.encrypt(response)
		h = hashlib.md5()
		h.update(encryptedResponse)
		newMD5Sum = h.hexdigest()
		token = (encryptedResponse, newMD5Sum)

		print("[" + str(datetime.datetime.now())  + "] [Checkpoint " + str(checkpoint).zfill(2) + "] Encrypt: Key: " + str(key) + " | Ciphertext: " + str(token))
		checkpoint += 1
		
		print("[" + str(datetime.datetime.now())  + "] [Checkpoint " + str(checkpoint).zfill(2) + "] Generated MD5 Checksum: " + str(newMD5Sum))
		checkpoint += 1
		
		pickleAns = pickle.dumps(token)
		print("[" + str(datetime.datetime.now())  + "] [Checkpoint " + str(checkpoint).zfill(2) + "] Sending answer: " + str(pickleAns))
		checkpoint += 1
		client.send(pickleAns)

		client.close()
		
