# Client

The Client is initialized with these parameters.

`python3 client.py -sip <SERVER_IP> -sp <SERVER_PORT> -z <SOCKET_SIZE>`

#### Example

`python3 client.py -sip 192.168.1.134 -sp 4444 -z 1024`

## Required Dependencies for Client (Libraries)

1. pygame
2. socket
3. pickle
4. cryptography
5. hashlib
6. picamera
7. __future__
8. time
9. numpy
10. cv2
11. pyzbar.pzbar
12. watson_developer_cloud

# Server

The Server is initialized with these parameters

`python3 server.py -sp <SERVER_PORT> -z <SOCKET_SIZE>`

#### Example

`python3 server.py -sp 5555 -z 1024`

## Required Dependencies for Server (Libraries)

1. socket
2. wolframalpha
3. cryptography
4. pickle
5. watson_developer_cloud
6. pygame
7. hashlib
8. datetime
