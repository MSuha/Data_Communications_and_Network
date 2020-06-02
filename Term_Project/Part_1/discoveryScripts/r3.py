import socket
import time
import threading
import logging

## IP's for R3 node
ip_get_r2 = "10.10.6.2" 
ip_send_r2 = "10.10.6.1"

ip_send_s = "10.10.3.1"
ip_get_s = "10.10.3.2"

ip_send_d = "10.10.7.1"
ip_get_d = "10.10.7.2"

#Ports for R3 node
port_r2= 32001
port_s = 35437
port_d = 45678

Message = "Sent by R3 "

#Sockets used in R3
sockS = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sockR2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sockD = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# RTT files relatively  
r3_r2 = open("r3_r2.txt","w+")
r3_s = open("r3_s.txt","w+")
r3_d = open("r3_d.txt","w+")

# Function to send S 1000 messages
def sendS(ip,port):
    for i in range(1000):
        print "Now sending " + str(i) + " with thread 1"  #to follow the threads in terminal
        start = time.time()
        sockS.sendto(Message + str(i), (ip, port)) #sending the message
        try:
            data, server = sockS.recvfrom(1024) #waiting for ACK 
            end = time.time()
        except: 
            print "Error occured in R3-S" #NACK or Timeout
        diff = end-start
        r3_s.write(str(diff)+ '\n')
        print "Finished sending " + str(i) + " with thread 1"

# Function to send D 1000 messages
def sendD(ip,port):
    for i in range(1000):
        print "Now sending " + str(i) + " with thread 2"  #to follow the threads in terminal
        start = time.time()
        sockD.sendto(Message + str(i), (ip, port))  #sending the message
        try:
            data, server = sockD.recvfrom(1024) #waiting for ACK 
            end = time.time()
        except: 
            print "Error occured in R3-D" #NACK or Timeout
        diff = end-start
        r3_d.write(str(diff)+ '\n')
        print "Finished sending " + str(i) + " with thread 2"

# Function to send R2 1000 messages
def sendR2(ip,port):
    for i in range(1000):
        print "Now sending " + str(i) + " with thread 3"  #to follow the threads in terminal
        start = time.time()
        sockR2.sendto(Message + str(i), (ip, port)) #sending the message
        try:
            data, server = sockR2.recvfrom(1024) #waiting for ACK 
            end = time.time()
        except: 
            print "Error occured in R3-R2" #NACK or Timeout
        diff = end-start
        r3_r2.write(str(diff)+ '\n')
        print "Finished sending " + str(i) + " with thread 3"

## SummationCalculator function is defined for to the summation of each 1000 RTT's seperately.
def sumCalc(a):
    f = open(a,"r")
    average = 0
    for line in f:
        average += float(line.strip('\n'))   #casting string time diffence to float
    wrt = open("sum.txt","a") #appending to the file
    wrt.write("Sum for " + a + " is : "+ str(average) +"\n") 
    wrt.close()

if __name__ == "__main__":

    t1 = threading.Thread(target=sendS, args=(ip_send_s,port_s)) 
    t2 = threading.Thread(target=sendD, args=(ip_send_d,port_d)) 
    t3 = threading.Thread(target=sendR2, args=(ip_send_r2,port_r2)) 
  
    # starting thread 1 
    t1.start() 
    # starting thread 2 
    t2.start() 
     # starting thread 3 
    t3.start()
    # wait until thread 1 is completely executed 
    t1.join() 
    # wait until thread 2 is completely executed 
    t2.join() 
    # wait until thread 3 is completely executed 
    t3.join()

    # print t1.isAlive()
    # print t2.isAlive()
    # print t3.isAlive()

    # both threads completely executed 
    print("Done!") 

    #After threads are DONE, close the files,
    r3_d.close()
    r3_s.close()
    r3_r2.close()

    #and calculate their summations, seperately.
    sumCalc("r3_r2.txt")
    sumCalc("r3_s.txt")
    sumCalc("r3_d.txt")
