import socket
import sys
import wolframalpha
from cryptography.fernet import Fernet
import ServerKeys 
import pickle
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
	port = int(sys.argv[2])
	backlog = 5
	size = int(sys.argv[4])
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#	s.bind((host,port))
	s.listen(backlog)
	print("[Checkpoint " + str(checkpoint).zfill(2) + "] Created socket at " + str(host) + " on port " + str(port))
	checkpoint += 1
	print("[Checkpoint " + str(checkpoint).zfill(2) + "] Listening for client connections")
	checkpoint += 1
	while 1:
		client, address = s.accept()
		print("[Checkpoint " + str(checkpoint).zfill(2) + "] Accepted client connection from  " + str(address) + " on port " + str(port))
		checkpoint += 1
		data = client.recv(size)
		print("[Checkpoint " + str(checkpoint).zfill(2) + "] Received data:  " + str(data))
		checkpoint += 1
		unpickled = pickle.loads(data)
		key = unpickled[0]
		question = unpickled[1]
		hash = unpickled[2]
		actQuestion = key.decrypt(question)
		print("[Checkpoint " + str(checkpoint).zfill(2) + "] Decrypt: Key: " + str(key) + " | Plain text: " + str(question))		
		checkpoint += 1
		print("[Checkpoint " + str(checkpoint).zfill(2) + "] Speaking Question: " + str(actQuestion))
		checkpoint += 1
		print("[Checkpoint " + str(checkpoint).zfill(2) + "] Sending question to Wolframalpha " + str(actQuestion))
		checkpoint += 1
		response = wolfClient.query(actQuestion)		
		print("[Checkpoint " + str(checkpoint).zfill(2) + "] Received question from Wolframalpha " + str(response)) 
		checkpoint += 1
		token = key.decrypt(response)
		hash = hashlib.sha1(bytes(response, encoding= 'utf-8'))
		print("[Checkpoint " + str(checkpoint).zfill(2) + "] Encrypt: Key: " + key + " | Ciphertext: " + token)
		checkpoint += 1
		
		print("[Checkpoint " + str(checkpoint).zfill(2) + "] Generated MD5 Checksum: " + str(hash))
		checkpoint += 1
		tupAns = (token,hash)
		pickleAns = pickle.dumps(tupAns)
		print("[Checkpoint " + str(checkpoint).zfill(2) + "] Sending answer: " + pickleAns)
		
		client.send(pickleAns)

		client.close()
		
