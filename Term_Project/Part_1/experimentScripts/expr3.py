import socket
import time
import threading
import logging

#For the experiment we only needed S-R3-D implementation,
#so other ports are not implemented.

#R3 is between S and D , receives from S , sends to D
ip_send_s = "10.10.3.1"
ip_get_s = "10.10.3.2"

ip_send_d = "10.10.7.1"
ip_get_d = "10.10.7.2"

port_s = 35437
port_d = 45678

Message = "- Sent by R3- "

sockS = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sockD = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def getS():
    print "Now getting from S " 
    sockS.bind((ip_get_s,port_s)) #binding the ports
    try:
        datafromS, addressS = sockS.recvfrom(1024)  #waiting for data
    except: 
        print "Error occured in R3-S" #timeout

    print "Data received from S, now sending it to D"
    sockD.sendto(datafromS + Message, (ip_send_d,port_d)) #sends the received data from S to D
    try:
        datafromD, addressD = sockD.recvfrom(1024) #Waits for ACK from D
    except: 
        print "Error occured in R3-D"
    print "Data received from D, now sending it back to S"
    sockS.sendto(datafromD, addressS) #Sends ACK to S



if __name__ == "__main__":

    getS()

    print("Done!") 

