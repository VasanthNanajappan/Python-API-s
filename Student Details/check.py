from faker import Faker
from time import sleep
from threading import *

fake=Faker()

result = [None] * 10
def func(result,i):
    data=fake.name()
    result[i]=data

threads=[]
for i in range(5):
    process=Thread(target=func,args=[result,i])
    process.start()
    sleep(1)
    threads.append(process)


for i in range(5,10):
    process1=Thread(target=func,args=[result,i])
    process1.start()
    sleep(1)
    threads.append(process1)

for process in threads:
    process.join()


print(result)