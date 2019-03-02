#!/usr/bin/env python3

"""
A simple echo client
"""
import sys
import socket

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
	print("[Checkpoint " + str(checkpoint.zfill(2) + "] Connection to " + str(host) + " on port " + str(port)) 
	checkpoint += 1
	while 1:
		print("[Checkpoint " + str(checkpoint.zfill(2) + "] Listening for QR codes from RPi Camera that contain questions")
		checkpoint += 1
		
		s.send()
		data = s.recv(size)
		s.close()
		print ('Received:', data)
