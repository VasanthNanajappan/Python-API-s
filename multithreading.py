from time import sleep
from threading import *

class One(Thread):
    def run(self):
        for i in range(5):
            print("Hello")
            sleep(1)

class Two(Thread):
    def run(self):
        for i in range(5):
            print("Hi")
            sleep(1)

t1=One()
t2=Two()

t1.start()
sleep(0.2) #used to avoid collision
t2.start()