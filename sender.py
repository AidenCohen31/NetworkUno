import argparse
import socket
import struct
from datetime import datetime
import os

MAX_BYTES = 6000
class DataPacket:
    def __init__(self, s, raddr, rport, length, payload):
        self.s = s 
        self.raddr = raddr 
        self.length = length 
        self.payload = payload 
        self.time = datetime.now()
    def __repr__(self):
        return f"DATA Packet\nsend time:\t{self.time}\nrequester addr:\t{self.raddr}:{self.rport}\nSequence num:\t{self.s}\nlength:\t{self.length}\npayload:{self.payload}"



def receiveRequest(serversocket):
    data, addr = serversocket.recvfrom(MAX_BYTES)
    request = struct.unpack_from("!cII",data)
    length = request[2]
    fileName = struct.unpack_from(f"!{length}s",data,offset=9)[0].decode('utf-8')
    print("file name recieved : "+fileName)
    return fileName, addr



def readFile(filename, b):
    bytearr = []
    with open(filename, "rb") as f:
        while (byte := f.read(b)):
            bytearr.append(byte)
    return bytearr


def makeDataPacket(bytes, sequence_num):
    return struct.pack(f"!cII{len(bytes)}s",b'D',sequence_num,len(bytes),bytes)

def sendData(address,port, bytes, sequence_num):
    sock = socket.socket(socket.AF_INET,  socket.SOCK_DGRAM)
    sock.sendto(makeDataPacket(bytes,sequence_num), (address, port))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port")
    parser.add_argument("-g", "--requester_port")
    parser.add_argument("-r" "--rate")
    parser.add_argument("-q", "--seq_no")
    parser.add_argument("-l", "--length")
    args = parser.parse_args()
    
    serversocket = socket.socket(socket.AF_INET,  socket.SOCK_DGRAM)
    serversocket.bind((socket.gethostname(), int(args.port)))
    
    filename, address = receiveRequest(serversocket)
    sequence = int(args.seq_no)
    with open(filename,"r+b") as file:
        bytes = bytearray(file.read())
        for i in range(0,len(bytes),int(args.length)):
            section = bytes[i:min(i+int(args.length),len(bytes))]
            sendData(address[0],int(args.requester_port),section,sequence)
            sequence += len(section)
            print("Sent at: ",datetime.utcnow())
            print("Address: ",address[0])
            print("Port: ",int(args.requester_port))
            print("Sequence number ",sequence)
        

    serversocket.close()
