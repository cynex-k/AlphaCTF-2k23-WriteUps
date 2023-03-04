#!/usr/bin/python

def main():
#flag = O0ps_my_m3N_3y3s_0N_my_spy
#encoded_flag = E179623624C6434961C6236973    
    transformation_table = {
        0x7e: '0', 0x30: '1', 0x6d: '2',
        0x79: '3', 0x33: '4', 0x5b: '5',
        0x5f: '6', 0x70: '7', 0x7f: '8',
        0x73: '9', 0x77: 'A', 0x1f: 'b',
        0x4e: 'C', 0x3d: 'd', 0x4f: 'E',
        0x47: 'F'}

    dec = input("what do you want (encode/decode)? \nYour answer: ")
    if dec == 'encode':
        buf = input("[*] message > ")
        print('[*] Encoded message: ',end="")
        for i in range(len(buf)):
            asci = ord(buf[i])
            print(transformation_table[asci], end="")
    elif dec == 'decode':
        buf = input("[*] Encoded message > ")
        for i in range(len(buf)):
            for j in transformation_table:
                if buf[i] == transformation_table[j]:
                    print(chr(list(transformation_table.keys())[
                          list(transformation_table.values()).index(buf[i])]), end="")
    else:
        print('invalid choice')
        return


if __name__ == "__main__":
    main()
