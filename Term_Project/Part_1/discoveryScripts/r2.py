import socket
import time
import threading
#import logging

## IP's for R2 node
ip_get_r1 = "10.10.8.2"  
ip_send_r1 = "10.10.8.1" 

ip_send_s = "10.10.2.2"
ip_get_s = "10.10.2.1"

ip_send_d = "10.10.5.2"
ip_get_d = "10.10.5.1"

ip_get_r3 = "10.10.6.1"
ip_send_r3 = "10.10.6.2"

#Ports for R2 node
port_r1 = 32984 
port_r3 = 32001
port_s = 35436
port_d = 44004

Message = "Sent by R2 "

#Sockets used in R2
sockS = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sockR1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sockD = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sockR3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# RTT files relatively 
r2_s = open("r2_s.txt","w+")
r2_d = open("r2_d.txt","w+")


# Function to send S 1000 messages
def sendS(ip,port):
    for i in range(1000):
        print "Now sending " + str(i) + "with thread 1" #to follow the threads in terminal
        start = time.time()
        sockS.sendto(Message + str(i), (ip, port)) #sending the message
        try:
            data, server = sockS.recvfrom(1024) #waiting for ACK 
            end = time.time()
        except: 
            print "Error occured in R2-S" #NACK or Timeout
        diff = end-start
        r2_s.write(str(diff)+ '\n')
        print "Finished sending " + str(i) + "with thread 1"

# Function to send D 1000 messages
def sendD(ip,port):
    for i in range(1000):
        print "Now sending " + str(i) + "with thread 2" #to follow the threads in terminal
        start = time.time()
        sockD.sendto(Message + str(i), (ip, port)) #sending the message
        try:
            data, server = sockD.recvfrom(1024) #waiting for ACK 
            end = time.time()
        except: 
            print "Error occured in R2-D" #NACK or Timeout
        diff = end-start
        r2_d.write(str(diff)+ '\n')
        print "Finished sending " + str(i) + "with thread 2"

# Function to receive 1000 messages from R1
def getR1(ip,port):
    sockR1.bind((ip,port)) #Binding of get port between r1-r2
    i  =1000
    while i:
        data, addr = sockR1.recvfrom(1024) # Waiting 1000 messages from R1
        print "Message: ", data
        sockR1.sendto(data, addr)   #Sending ACK after receiving 
        i -= 1

# Function to receive 1000 messages from R3
def getR3(ip,port):
    sockR3.bind((ip,port)) #Binding of get port between r3-r2
    i  =1000
    while i:
        data, addr = sockR3.recvfrom(1024) # Waiting 1000 messages from R3
        print "Message: ", data
        sockR3.sendto(data, addr) #Sending ACK after receiving 
        i -= 1

# SummationCalculator function is defined for to the summation of each 1000 RTT's seperately.
def sumCalc(a):
    f = open(a,"r")
    average = 0
    for line in f:
        average += float(line.strip('\n'))  #casting string time diffence to float
    wrt = open("sum.txt","a")  #appending to the file
    wrt.write("Sum for " + a + " is : "+ str(average) +"\n")
    wrt.close()

if __name__ == "__main__":

    #Threads (target= calling function for that thread, args = arguments given to each function)
    t1 = threading.Thread(target=sendS, args=(ip_send_s,port_s)) 
    t2 = threading.Thread(target=sendD, args=(ip_send_d,port_d)) 
    t3 = threading.Thread(target=getR1, args=(ip_get_r1,port_r1)) 
    t4 = threading.Thread(target=getR3, args=(ip_get_r3,port_r3)) 

    # starting thread 1 
    t1.start() 
    # starting thread 2 
    t2.start() 
    # starting thread 3
    t3.start()
    # starting thread 4 
    t4.start()
    # wait until thread 1 is completely executed 
    t1.join() 
    # wait until thread 2 is completely executed 
    t2.join() 
     # wait until thread 3 is completely executed 
    t3.join()
     # wait until thread 4 is completely executed 
    t4.join()

    # print t1.isAlive()
    # print t2.isAlive()
    # print t3.isAlive()
    # print t4.isAlive()
    # both threads completely executed 
    print("Done!") 
 
    #After threads are DONE, close the files,
    r2_d.close()
    r2_s.close()

    #and calculate their summations, seperately.
    sumCalc("r2_d.txt")
    sumCalc("r2_s.txt")

