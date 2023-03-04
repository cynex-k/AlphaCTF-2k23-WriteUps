import socket
import time
from pwn import * 
import random
from hashlib import md5

MOD = 1 << 16
def geneFlag():
    flag = b'AlphaCTF{' + md5(str(random.randint(0,255)).encode()).hexdigest().encode() + b'}'
    return list(flag)

def to_bin(i):
    return bin(int(i,16))[2:].zfill(16)
    
def ones_comp_add16(num1,num2):
    result = num1 + num2
    return result if result < MOD else (result+1) % MOD

def checksum(data):
    binarynums = []
    for i in range(0,len(data),2):
        tmp =data[i:i+2].hex()
        if len(tmp) < 4: tmp +='00'
        binarynums.append(to_bin(tmp))
    res = 0b000000000000000
    # print(binarynums)
    for j in binarynums:
        res = ones_comp_add16(res, int(j,2))
    return bytes.fromhex(hex(0xffff-res)[2:].zfill(4))



s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
def ping(source,destination,id,seq,data):
    tmp = source.split(".")
    addr_src = b''
    for i in tmp:

        addr_src+= bytes.fromhex(hex(int(i))[2:].zfill(2))
    tmp = destination.split(".")
    addr_dst = b''
    for i in tmp:
        addr_dst+= bytes.fromhex(hex(int(i))[2:].zfill(2))

    ip_header = b'\x45\x20\x00\x1c' # Version, IHL, Type of Service | Total Length
    ip_header += b'\xab\xcd\x00\x00' # Identification | Flags, Fragment Offset
    ip_header += b'\x40\x01\x6b\xd8' # TTL, Protocol | Header Checksum
    ip_header +=  addr_src           #b'\xc0\xa8\x76\xe4' # Source Address
    ip_header += addr_dst            #b'\x08\x08\x08\x08' # Destination Address

    icmp_header = b'\x08\x00\x00\x00' # Type of message, Code | Checksum
    icmp_header += id + bytes.fromhex(seq.zfill(4)) # Identifier | Sequence Number
    icmp_header += p64(round(time.time())) # timestamp
    icmp_header += data  #b'hello' # Payload Data
    check = checksum(icmp_header)
    icmp_header = icmp_header[0:2] + check + icmp_header[4:]
    return ip_header + icmp_header

f  = open("flag.png","rb")
data = f.read()
f.close()
data = [data[i:i+2] for i in range(0, len(data), 2)]
dic = {}
for i ,name in enumerate(data):
    dic[i]=name
keys = list(dic.keys())
random.shuffle(keys)
shuffled_dict = {key: dic[key] for key in keys}
shuffled_keys = list(shuffled_dict.keys())

addr_src = "192.168.14.132"
addr_dst = "192.168.14.243"

flag = geneFlag()
for i in range(len(shuffled_keys)):
    if i > len(flag):
        flag = geneFlag()
    s.sendto(ping(addr_src, addr_dst, shuffled_dict[shuffled_keys[i]],str(hex(shuffled_keys[i]))[2:] , str(flag[i % len(flag)]).encode()), ('192.168.14.243', 0))
    sleep(0.1)
