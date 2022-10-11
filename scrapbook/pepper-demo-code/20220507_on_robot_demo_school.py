from pepper.robot import Pepper
import random, os, time
import qi

ip_address = "192.168.1.200"
port = 9559
robot = Pepper(ip_address, port)

robot.set_english_language()
robot.set_volume(50)
robot.say("Hello, I am Pepper robot. I am currently at Loughborough University")

robot.start_animation("Hey_1")

robot.say("I can take a picture of you")
robot.take_picture()

robot.say("I can also show any internet page on my tablet.")
robot.show_web("https://www.google.com/")
time.sleep(5)
robot.reset_tablet()

robot.say("Do you want to try the google speech recognition library with me?")
positive_answers = ["yes", "yep", "ok", "i want", "sure", "definitely"]
vocab = positive_answers + ["no", "not", "i dont", "i do not know", "not sure"]
answer = robot.listen_to(vocabulary=vocab)

if answer[0] in positive_answers:
      robot.say("Ok, please count up to five now")
      recognised = robot.recognize_google(lang="en-US")
      robot.say("I recognized {}".format(recognised.encode('utf-8')))
else: robot.say("Cool.")

import socket

try:
  s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s1.connect(("192.168.1.101", 65432))
  print("connected to robot1")
except:
  s1 = None
  print("robot 1 not connected!")

robot.say("I have many robotic friends, For example Robot jetson")
robot.say("Hello, jetson, Can you move forward")
if s1:
  s1.sendall(b"1")

time.sleep(2)
robot.say("jetson, Can you move right")
if s1:
  s1.sendall(b"2")

time.sleep(2)
robot.say("jetson, Can you move left")
if s1:
  s1.sendall(b"3")

time.sleep(2)
robot.say("jetson, Can you move backward")
if s1:
  s1.sendall(b"4")

time.sleep(2)
robot.say("Can you make a dance for our friends")
if s1:
  time.sleep(0.5)
  s1.sendall(b"2")
  time.sleep(0.5)
  s1.sendall(b"2")
  time.sleep(0.5)
  s1.sendall(b"3")
  time.sleep(0.5)
  s1.sendall(b"3")
  time.sleep(0.5)
  s1.sendall(b"2")
  time.sleep(0.5)
  s1.sendall(b"2")
  time.sleep(0.5)
  s1.sendall(b"3")
  time.sleep(0.5)
  s1.sendall(b"3")
  time.sleep(0.5)
  s1.sendall(b"2")
  time.sleep(0.5)
  s1.sendall(b"2")
  time.sleep(0.5)
  s1.sendall(b"3")
  time.sleep(0.5)
  s1.sendall(b"3")
  time.sleep(0.5)
  s1.sendall(b"2")
  time.sleep(0.5)
  s1.sendall(b"2")
  time.sleep(0.5)
  s1.sendall(b"3")
  time.sleep(0.5)
  s1.sendall(b"3")

time.sleep(1)
robot.say("Thank you jetson")