

MOD = 1 << 16
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

    for j in binarynums:
        res = ones_comp_add16(res, int(j,2))
    hex(0xffff-res)

payload = ""



# data = b"\x08\x00\x00\x00\x12\x34\x00\x01"
data = b"\x08\x00\x00\x00\x12\x34\x00\x01hello"
