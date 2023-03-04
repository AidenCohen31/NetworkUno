import argparse 
import socket
import struct
import csv
from collections import defaultdict

MAX_BYTES = 6000

def makeRequestPacket(filename):
    byteString =bytes(filename,'utf-8')
    return struct.pack(f"!cII{len(byteString)}s",b'R',0,len(byteString),byteString)

def sendRequest(hostName,port, filename):
    sock = socket.socket(socket.AF_INET,  socket.SOCK_DGRAM)
    sock.sendto(makeRequestPacket(filename), (hostName, port))

def receivePacket(sock):
    data, addr = sock.recvfrom(MAX_BYTES)
    header = struct.unpack_from("!cII",data)
    length = header[2]
    payload = struct.unpack_from(f"!{length}s",data,offset=9)[0].decode('utf-8')
    print("Data recieved : "+payload)
    return payload


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

    sock = socket.socket(socket.AF_INET,  socket.SOCK_DGRAM)
    sock.bind((socket.gethostname(), int(args.port)))
    for i in d[args.fileoption]:
        id = i[0]
        #hostname, port, filename
        sendRequest(i[1],i[2],args.fileoption)
        text = receivePacket(sock)
        print(text)

