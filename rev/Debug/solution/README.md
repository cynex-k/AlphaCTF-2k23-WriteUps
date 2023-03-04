# Debug

**`Author:`** [Cynex](https://github.com/cynex-k)

## Description:
> Do you think you can Debug this program you better think TWICE.

## Attachment:
[Chall](../challenge/chall)

## Solution:

### First:

we run a file command on the binary file : 

```
chall: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=8223827ec032a461c5c15876fb29479bdc9edda1, for GNU/Linux 3.2.0, not stripped
```
We see that it is an ELF (Executable and Linkable Format) with 64 bit arch, Dynamically linked which means it calls the libraries since they are inside the binary itself and not stripped which means that we still can see clearly the name of functions as they were in the source code.

### Second:

We run the file (Do not forget to make it executable with this command `chmod +x ./chall `) 

```
cynex@kali:$./chall  
Give me the password dude:
aaaaaaa
Nah not the write password try harder!!
```
So we know that the binary prints `Give me the password dude:` then take an input from `stdin` then do some of comparison then prints a String based on a Result
So our goal is to find the right password maybe to gain the flag

### Third:

we open [ghidra](https://ghidra-sre.org/) to examine our binary we import it then we look to the main function 

```c
undefined8 main(void)

{
  byte abStack_100 [8];
  undefined8 alphactf_;
  undefined8 local_f0;
  undefined4 local_e8;
  char local_e2 [10];
  long input [8];
  char local_98 [80];
  ulong *local_48;
  FILE *local_40;
  int local_34;
  undefined4 local_30;
  uint local_2c;
  code *main;
  uint j;
  uint i;
  int local_14;
  int local_10;
  uint local_c;
  
  main = ::main;
  local_2c = 0;
  local_10 = 0;
  local_14 = 0;
  alphactf_ = 0x4654436168706c41;
  local_f0 = 0x5f;
  local_e8 = 0;
  local_30 = 0x13371337;
  for (i = 0; i < 8; i = i + 1) {
    abStack_100[i] = 0x13371337 >> (i << 3 & 0x1f);
  }
  setbuf(stdin,0x0);
  setbuf(stdout,0x0);
  puts("Give me the password dude:");
  fgets(input,0x40,stdin);
  for (; *(input + local_14) != '\n'; local_14 = local_14 + 1) {
  }
  *(input + local_14) = 0;
  for (j = 0; *(input + j) != '\0'; j = j + 1) {
    *(input + j) = *(input + j) ^ abStack_100[j & 7];
  }
  res = input[0];
  while (local_c != 0xc3) {
    local_48 = main + local_10;
    local_2c = *local_48;
    local_c = local_2c & 0xff;
    if ((*local_48 & 0xff) != 0) {
      res = res + (local_c << 4);
    }
    local_10 = local_10 + 1;
  }
  sprintf(local_e2,"%lx",res);
  strcat(&alphactf_,local_e2);
  local_34 = strncmp(&alphactf_,"AlphaCTF_a4cf9924a7a50fe9",0x11);
  if (local_34 == 0) {
    local_40 = fopen("flag.txt","r");
    fgets(local_98,0x47,local_40);
    printf("Good job dude here is your prize: %s\n",local_98);
    fclose(local_40);
    return 0;
  }
  puts("Nah not the write password try harder!!");
                    /* WARNING: Subroutine does not return */
  exit(1);
}
```
 
 Now we start static analyse in the beginning we see a FOR loop that is just moving each byte of `0x13371337` to a table named by ghidra `abStack_100` 
 
 ```c
 for (i = 0; i < 8; i = i + 1) {
    abStack_100[i] = 0x13371337 >> (i << 3 & 0x1f);
  }
```
so after this the table will look like this  `abStack_100 = [0x13,0x37,0x13,0x37]`

After that setting buf and printing the first string then gets the input from the `stdin` and put it in variable called `input` (you can change the name of variable in ghidra by selecting the variable then hit the key `L`  it helps to make the code more readable)  

In this part of code:
```c
for (; *(input + local_14) != '\n'; local_14 = local_14 + 1) {
  }
  *(input + local_14) = 0;
```
we see that we loop in the our input until we find the `\n` (newline) then replace it with null byte `\0`  

Now we have this:
```c
  for (j = 0; *(input + j) != '\0'; j = j + 1) {
    *(input + j) = *(input + j) ^ abStack_100[j & 7];
  }
  res = input[0];
```
we are making XOR `^` operation to the input with the table `abStack_100` 
then we assign the address of the input to the `res` variable

Moving on :
```c
while (local_c != 0xc3) {
    local_48 = main + local_10;
    local_2c = *local_48;
    local_c = local_2c & 0xff;
    if ((*local_48 & 0xff) != 0) {
      res = res + (local_c << 4);
    }
    local_10 = local_10 + 1;
  }
```
In this while loop we see that `local_48` get the address of the main of our binary 
then `local_2c` take the value of the address `local_48` meaning that we are taking the instructions of main as byte 
we shift it by 4 then we add it to the `res` variable then we increment the `local_10` until we get `0xc3`. There is a trick here some people will think that we are looping in all the intructions of the main because of `0xc3` is the `ret` instruction in asm but will forget that  in this condition 
`local_c != 0xc3` we are using `0xc3`. So are taking the instructions from the beginning of main until this conditon 

Finally:
```c
  sprintf(local_e2,"%lx",res);
  strcat(&alphactf_,local_e2);
  local_34 = strncmp(&alphactf_,"AlphaCTF_a4cf9924a7a50fe9",0x11);
  if (local_34 == 0) {
    local_40 = fopen("flag.txt","r");
    fgets(local_98,0x47,local_40);
    printf("Good job dude here is your prize: %s\n",local_98);
    fclose(local_40);
    return 0;
  
```
The result of shifting and adding put in the `local_e2` as long hexadecimal notation (`%lx`) then we concatente it with the string `AlphaCTF_`
After that we compare it with `AlphaCTF_a4cf9924a7a50fe9`
if it returns 0 (which means they are identical) will get the flag for us otherwise we get the error message then we exit.

### Fourth:
our plan now: 
1- Bring the compared value.
2- Bring the bytes of the main function
3- Subtract the compared value with main function bytes after we shift it 
4 - Make XOR operation with `0x13371337`

For the compared vlaue `0xa4cf9924a7a50fe9` 
we can bring the the bytes using the commad `objdump` 
```
objdump -d chall -mi386:x86-64:intel --start-address=0x1232 --stop-address=0x13ed --show-raw-insn
```
Now we can create python script that brings us the right input

```py
res = 0xa4cf9924a7a50fe9

data = [0x55, 0x48, 0x89, 0xe5, 0x48, 0x81, 0xec, 0x10, 0x01, 0x00, 0x00, 0x89, 0xbd, 0xfc, 0xfe, 0xff, 0xff, 0x48, 0x89, 0xb5, 0xf0, 0xfe, 0xff, 0xff, 0x48, 0x8d, 0x05, 0xe1, 0xff, 0xff, 0xff, 0x48, 0x89, 0x45, 0xe0, 0xc7, 0x45, 0xdc, 0x00, 0x00, 0x00, 0x00, 0xc7, 0x45, 0xf8, 0x00, 0x00, 0x00, 0x00, 0xc7, 0x45, 0xf4, 0x00, 0x00, 0x00, 0x00, 0x48, 0xb8, 0x41, 0x6c, 0x70, 0x68, 0x61, 0x43, 0x54, 0x46, 0xba, 0x5f, 0x00, 0x00, 0x00, 0x48, 0x89, 0x85, 0x10, 0xff, 0xff, 0xff, 0x48, 0x89, 0x95, 0x18, 0xff, 0xff, 0xff, 0xc7, 0x85, 0x20, 0xff, 0xff, 0xff, 0x00, 0x00, 0x00, 0x00, 0x8b, 0x05, 0xc9, 0x2d, 0x00, 0x00, 0x89, 0x45, 0xd8, 0xc7, 0x45, 0xf0, 0x00, 0x00, 0x00, 0x00, 0xeb, 0x21, 0x8b, 0x45, 0xf0, 0xc1, 0xe0, 0x03, 0x8b, 0x55, 0xd8, 0x89, 0xc1, 0xd3, 0xfa, 0x89, 0xd0, 0x89, 0xc2, 0x8b, 0x45, 0xf0, 0x48, 0x98, 0x88, 0x94, 0x05, 0x08, 0xff, 0xff, 0xff, 0x83, 0x45, 0xf0, 0x01, 0x8b, 0x45, 0xf0, 0x83, 0xf8, 0x07, 0x76, 0xd7, 0x48, 0x8b, 0x05, 0xad, 0x2d, 0x00, 0x00, 0xbe, 0x00, 0x00, 0x00, 0x00, 0x48, 0x89, 0xc7, 0xe8, 0x80, 0xfd, 0xff, 0xff, 0x48, 0x8b, 0x05, 0x89, 0x2d, 0x00, 0x00, 0xbe, 0x00, 0x00, 0x00, 0x00, 0x48, 0x89, 0xc7, 0xe8, 0x6c, 0xfd, 0xff, 0xff, 0x48, 0x8d, 0x05, 0x0d, 0x0d, 0x00, 0x00, 0x48, 0x89, 0xc7, 0xe8, 0x3d, 0xfd, 0xff, 0xff, 0x48, 0x8b, 0x15, 0x76, 0x2d, 0x00, 0x00, 0x48, 0x8d, 0x85,
        0x30, 0xff, 0xff, 0xff, 0xbe, 0x40, 0x00, 0x00, 0x00, 0x48, 0x89, 0xc7, 0xe8, 0x62, 0xfd, 0xff, 0xff, 0xeb, 0x04, 0x83, 0x45, 0xf4, 0x01, 0x8b, 0x45, 0xf4, 0x48, 0x98, 0x0f, 0xb6, 0x84, 0x05, 0x30, 0xff, 0xff, 0xff, 0x3c, 0x0a, 0x75, 0xeb, 0x8b, 0x45, 0xf4, 0x48, 0x98, 0xc6, 0x84, 0x05, 0x30, 0xff, 0xff, 0xff, 0x00, 0xc7, 0x45, 0xec, 0x00, 0x00, 0x00, 0x00, 0xeb, 0x2f, 0x8b, 0x45, 0xec, 0x48, 0x98, 0x0f, 0xb6, 0x94, 0x05, 0x30, 0xff, 0xff, 0xff, 0x8b, 0x45, 0xec, 0x48, 0x98, 0x83, 0xe0, 0x07, 0x0f, 0xb6, 0x84, 0x05, 0x08, 0xff, 0xff, 0xff, 0x31, 0xc2, 0x8b, 0x45, 0xec, 0x48, 0x98, 0x88, 0x94, 0x05, 0x30, 0xff, 0xff, 0xff, 0x83, 0x45, 0xec, 0x01, 0x8b, 0x45, 0xec, 0x48, 0x98, 0x0f, 0xb6, 0x84, 0x05, 0x30, 0xff, 0xff, 0xff, 0x84, 0xc0, 0x75, 0xc0, 0x48, 0x8d, 0x85, 0x30, 0xff, 0xff, 0xff, 0x48, 0x8b, 0x00, 0x48, 0x89, 0x05, 0xf4, 0x2c, 0x00, 0x00, 0xeb, 0x48, 0x8b, 0x45, 0xf8, 0x48, 0x63, 0xd0, 0x48, 0x8b, 0x45, 0xe0, 0x48, 0x01, 0xd0, 0x48, 0x89, 0x45, 0xc0, 0x48, 0x8b, 0x45, 0xc0, 0x48, 0x8b, 0x00, 0x89, 0x45, 0xdc, 0x8b, 0x45, 0xdc, 0x0f, 0xb6, 0xc0, 0x89, 0x45, 0xfc, 0x83, 0x7d, 0xfc, 0x00, 0x74, 0x1a, 0x8b, 0x45, 0xfc, 0xc1, 0xe0, 0x04, 0x48, 0x63, 0xd0, 0x48, 0x8b, 0x05, 0xb8, 0x2c, 0x00, 0x00, 0x48, 0x01, 0xd0, 0x48, 0x89, 0x05, 0xae, 0x2c, 0x00, 0x00, 0x83, 0x45, 0xf8, 0x01, 0x81, 0x7d, 0xfc, 0xc3]
for i in data:
    if i != 0:
        res -= (i<<4)
print(bytes.fromhex(str(hex(res ^ 0x1337133713371337))[2:])[::-1])
```

But after running the script and test the word still we getting wrong. What do we miss?

If we back to ghidra and see the other functions we get this intersting function named 
"do_global_ctors_aux" 
You should configure your ghidra to uncheck "Eliminate unreachable code" by going to 
	"Edit-> Tool Option...-> Decompiler -> Analysis"
```c

void __do_global_ctors_aux(void)

{
  long lVar1;
  int local_14;
  int *local_10;
  
  syscall();
  if (false) {
    while ((local_14 < 0x100 && (*local_10 != 0x13371337))) {
      lVar1 = local_14;
      local_14 = local_14 + 1;
      local_10 = &data_start + lVar1 * 8;
    }
    *local_10 = -0x3c4524e9;
  }
  return;
}
```
This type of function runs before the main function 
first it calls syscall function we need to see the assembly code to know which syscall was called 
```asm
        001011cd b8 65 00        MOV        EAX,0x65
                 00 00
        001011d2 be 00 00        MOV        ESI,0x0
                 00 00
        001011d7 bf 00 00        MOV        EDI,0x0
                 00 00
        001011dc ba 00 00        MOV        EDX,0x0
                 00 00
        001011e1 0f 05           SYSCALL

```
We can now based on the registre EAX know the syscall using this [table](https://blog.rchapman.org/posts/Linux_System_Call_Table_for_x86_64/)  
(0x65)<sub>16</sub>= (101)<sub>10</sub>  we find the ptrace signal
Ptrace:(From linux man page):
	 (the "tracer") may observe and control the execution of another
       process (the "tracee"), and examine and change the tracee's
       memory and registers.  It is primarily used to implement
       breakpoint debugging and system call tracing.

Based on the return of the ptrace syscall it returns 0 if no one control the process of the program (if you use gdb it will fails )
it replace the the global variable that has `0x13371337` with `0xc3badb17`
we return to our script we replace with the right value 
run it and get the password 
```
N0-d3Bug
```
we submit that to the server using nc command then we get the flag

## Flag:
AlphaCTF{x0R_pTR4c3_w1tH0ut_bR3ak!\_m4n_g00dJOb}

