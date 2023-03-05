# Weird

**`Author:`** [Cynex](https://github.com/cynex-k)

## Description
  > numbers are weird when it comes to programming..    

## Attachment
[Weird](./challenge/weird)

## Solution
Let's take a look at the binary.
```
$ file weird

weird: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=2468410a0deafc941e8808a5db44c4a1b38fa6b6, for GNU/Linux 3.2.0, not stripped


$ checksec weird
[*] '/home/cynex/challengs/pwn/test/weird/solution/weird'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      PIE enabled

$ ./weird
Hello Hacker here is a easy one can you make it leet:145
Nah

```
So we can see that we are dealing with a `64` bit binary. When we look at the main function in Ghidra we see this:
```c

undefined8 main(void)

{
  char *pcVar1;
  char local_118 [64];
  char local_d8 [64];
  char input [112];
  FILE *local_28;
  float inputFloat;
  int result;
  int local_14;
  int neg_sign;
  int input_as_number;
  
  input_as_number = 0;
  local_14 = 2000;
  result = 0;
  neg_sign = 1;
  printf("Hello Hacker here is a easy one can you make it leet:");
  fgets(input,100,stdin);
  if (input[0] == '-') {
    neg_sign = -1;
  }
  input_as_number = atoi(input);
  if (neg_sign == -1) {
    input_as_number = -input_as_number;
  }
  result = input_as_number + local_14;
  if (result == 0x539) {
    printf("Good job this one is easier all you have to do is find the solution: ");
    fgets(local_d8,0x32,stdin);
    inputFloat = strtof(local_d8,0x0);
    if (36.35928 < inputFloat) {
      puts("This is Low!!!!!");
                    /* WARNING: Subroutine does not return */
      exit(0);
    }
    if (36.35928 < inputFloat) {
      puts("This is High!!!!!");
                    /* WARNING: Subroutine does not return */
      exit(0);
    }
    local_28 = fopen("flag.txt","r");
    if (local_28 == 0x0) {
      puts("Error: unable to open file.");
                    /* WARNING: Subroutine does not return */
      exit(0);
    }
    while( true ) {
      pcVar1 = fgets(local_118,0x32,local_28);
      if (pcVar1 == 0x0) break;
      printf("%s",local_118);
    }
    fclose(local_28);
  }
  else {
    puts("Nah");
  }
  return 0;
}
```
We can divide this binary in two stages 

### Stage 1 
we see that when we provide with a input it checks if it is negative by checking the first char of the input and convert it to positive if it is the case then add to `2000` then check the result with `1337` so we need to enter a positive number in which the program pass the negative check but at the end it see it as negative number 
This vuln called IntegerOverflow 
The range of an int in C is `-2147483648 to 2147483647`  (2^32/2) if we enter a number bigger than `2147483647` it will consider it as negative number for that we provide this input 
`2147483648 - 663+ 1 +2147483647 = 4294966633` it consider it as `-663` which is our solution 

### Stage 2 (weird float)
So we can see that the input we gave it is converted to a float. If it is greater than or less than `36.35928345`, the program will exit. We can see that if it doesn't exit, then it will scan in the contents of `flag.txt` and print it (thus we get the flag). However there is one issue. The value `36.35928345` contains more decimal places than a float handles, so we can get the number `36.35928345` to pass those checks:
```
$ ./weird
Hello Hacker here is a easy one can you make it leet:4294966633 
Good job this one is easier all you have to do is find the solution: 36.35928345
This is Low!!!!!
```

So we can't pass in the number `36.35928345` which is the only number not greater than or less than `36.35928345`. However we can still fail both checks. Floats have a special value called `nan` (stands for not a number). If the float is not a number, it will not be greater than, less than, or equal to `36.35928345` since it isn't a number. With that we can fail both checks and get the flag:
```
$ ./weird
Hello Hacker here is a easy one can you make it leet:4294966633 
Good job this one is easier all you have to do is find the solution: nan
AlphaCTF{1nT3g3R_OVerfL0w_w1TH_W3iRD_flOA7}
```

## Falg 
AlphaCTF{1nT3g3R_OVerfL0w_w1TH_W3iRD_flOA7}

