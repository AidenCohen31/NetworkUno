import argparse 
import socket
import struct
import csv
from collections import defaultdict
def makeRequestPacket(filename):
    byteString =bytes(filename,'utf-8')
    return struct.pack(f"!cII{len(byteString)}s",b'R',0,len(byteString),byteString)

def sendRequest(hostName,port, filename):
    serversocket = socket.socket(socket.AF_INET,  socket.SOCK_DGRAM)
    serversocket.sendto(makeRequestPacket(filename), (hostName, port))

def receivePacket(port):
    serversocket = socket.socket(socket.AF_INET,  socket.SOCK_DGRAM)
    serversocket.bind((socket.gethostname(), port))
    while True:
        data, addr = serversocket.recvfrom(5000)
        print("Hello %s" %data)

def constructString(data, file):
    pass

def parseTracker():
    with open("tracker.txt", "r") as f:
        d = defaultdict(lambda : [])
        reader = csv.reader(f,delimiter=' ')
        for row in reader:
            d[row[0]].append((int(row[1]), row[2], int(row[3])))
        
    for key in d.keys():
        d[key] = sorted(d[key], key =lambda x: x[0])
    return d



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port")
    parser.add_argument("-o", "--fileoption")
    args = parser.parse_args()
    d = parseTracker()
    for i in d[args.fileoption]:
        print(i)
        print(args.fileoption)
        sendRequest(i[1],i[2],args.fileoption)
        

