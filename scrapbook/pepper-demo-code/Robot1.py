from RobotClass import Robot
import time
import socket
HOST = "10.42.0.80"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

robot = Robot()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))

s.listen()
while True:
  print('waiting for connection ...')
  conn, addr = s.accept()

  print(f"Connected by {addr}")
  while True:
      data = conn.recv(1024)
      print(data)

      if not data:
          break
      #to prevent connection from stopping
#         conn.sendall(b'robot1 received')

      if(data == b'1'):
          robot.forward(0.5)
      elif data == b'2':
          robot.right(0.5)
      elif data == b'3':
          robot.left(0.5)
      elif data == b'4':
          robot.backward(0.5)
      else:
          print('wrong direction')
      time.sleep(0.3)

      robot.stop()
