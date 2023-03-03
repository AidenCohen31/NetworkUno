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
    while True:
        sequence, address = receiveRequest(serversocket)

        #sendData(sequence,address,int(args.requester_port))
