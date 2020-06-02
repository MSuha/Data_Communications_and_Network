import socket
import time
import threading

## IP's for R1 node
ip_get_r2 = "10.10.8.1"  
ip_send_r2 = "10.10.8.2"

ip_send_s = "10.10.1.1"
ip_get_s = "10.10.1.2"

ip_send_d = "10.10.4.2"
ip_get_d = "10.10.4.1"

#Ports for R1 node
port_r2= 32984  
port_s = 35435  
port_d = 23426

Message = "Sent by R1 "

#Sockets used in R1
sockS = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sockR2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sockD = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# RTT files relatively  
r1_r2 = open("r1_r2.txt","w+")
r1_s = open("r1_s.txt","w+")
r1_d = open("r1_d.txt","w+")

# Function to send S 1000 messages
def sendS(ip,port):
    for i in range(1000):
        print "Now sending " + str(i) + " with thread 1"  #to follow the threads in terminal
        start = time.time()
        sockS.sendto(Message + str(i), (ip, port))  #sending the message
        try:
            data, server = sockS.recvfrom(1024) #waiting for ACK 
            end = time.time() 
        except: 
            print "Error occured in R1-S" #NACK or Timeout
        diff = end-start
        r1_s.write(str(diff)+ '\n')
        print "Finished sending " + str(i) + " with thread 1"


# Function to send D 1000 messages
def sendD(ip,port):
    for i in range(1000):
        print "Now sending " + str(i) + " with thread 2" #to follow the threads in terminal
        start = time.time()
        sockD.sendto(Message + str(i), (ip, port))  #sending the message
        try:
            data, server = sockD.recvfrom(1024) #waiting for ACK 
            end = time.time()
        except: 
            print "Error occured in R1-D"  #NACK or Timeout
        diff = end-start
        r1_d.write(str(diff)+ '\n')
        print "Finished sending " + str(i) + " with thread 2"

# Function to send R2 1000 messages
def sendR2(ip,port):
    for i in range(1000):
        print "Now sending " + str(i) + " with thread 3" #to follow the threads in terminal
        start = time.time()
        sockR2.sendto(Message + str(i), (ip, port))  #sending the message
        try:
            data, server = sockR2.recvfrom(1024) #waiting for ACK 
            end = time.time()
        except: 
            print "Error occured in R1-R2"  #NACK or Timeout
        diff = end-start
        r1_r2.write(str(diff)+ '\n')
        print "Finished sending " + str(i) + " with thread 3"


## SummationCalculator function is defined for to the summation of each 1000 RTT's seperately.
def sumCalc(a):
    f = open(a,"r")
    sum = 0
    for line in f:
        sum += float(line.strip('\n'))  #casting string time diffence to float
    wrt = open("sum.txt","a") #appending to the file
    wrt.write("Sum for " + a + " is : "+ str(average) +"\n")
    wrt.close()

if __name__ == "__main__":

    #Threads (target= calling function for that thread, args = arguments given to each function)
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

    #print t1.isAlive()
    #print t2.isAlive()
    #print t3.isAlive()

    # both threads completely executed 
    print("Done!") 

    
    #After threads are DONE, close the files,
    r1_r2.close()
    r1_s.close()
    r1_d.close()
    #and calculate their summations, seperately.
    sumCalc("r1_r2.txt")
    sumCalc("r1_s.txt")
    sumCalc("r1_d.txt")