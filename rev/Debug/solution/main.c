#include <stdio.h>
#include <stdlib.h>
#include <sys/ptrace.h>
#include <sys/syscall.h>
#include <string.h>
extern globalvar;
globalvar = 0x13371337;
long int res = 0;

extern void *data_start;
void __attribute__((constructor)) __do_global_ctors_aux()
{
    ssize_t dst;
    register long rsp asm("rsp");
    asm("mov $0x65,%eax");
    asm("mov $0,%esi ");
    asm("mov $0,%edi ");
    asm("mov $0,%edx ");
    asm volatile("syscall"
                 : "=a"(dst));
    asm(""
        : "=r"(rsp));
    if (!(dst))
    {
        int *a, i;
        while (i < 0x100 && (*a != 0x13371337))
        {
            a = &data_start + i;
            i++;
        }
        *a = 0xc3badb17;
    }
}

int main(int argc, char *argv[])
{
    long *ptr = *main;
    long *adr;
    int one;
    int tmp = 0;
    int i = 0;
    int j = 0;
    FILE *stream;
    char flag[72];
    char buf[64];
    char str[10];
    char password[20] = "AlphaCTF_";
    int cmp;
    unsigned char bytes[sizeof(long)];
    int l = globalvar;
    for (int j = 0; j < sizeof(long); j++)
    {
            bytes[j] = (l >> (j * 8)) & 0xff;
    }
    setbuf(stdin, 0);
    setbuf(stdout, 0);
    puts("Give me the password dude:");
    fgets(buf, 0x40, stdin);
    while (buf[j] != '\n')
    {
        j++;
    }
    buf[j] = '\0';
    for (int k = 0; buf[k] != '\0'; k++)
    {
        buf[k] ^= bytes[k % sizeof(bytes)];
    }
    res = *(long *) buf;
    while (one != 0xc3)
    {
        adr = (void *)ptr + i;
        tmp = *adr;
        one = tmp & 0xff;
        if (one != 0x0)
        {
            res += one << 4;
        }
        i++;
    }
    sprintf(str, "%lx", res);
    strcat(password, str);
    int result = strncmp(password, "AlphaCTF_a4cf9924a7a50fe9", 17);
    if (result == 0)
    {
        stream = fopen("flag.txt", "r");
        fgets(flag, 71, stream);
        printf("Good job dude here is your prize: %s\n", flag);
        fclose(stream);
    }
    else
    {
        puts("Nah not the write password try harder!!");
        exit(1);
    }
    return 0;
}
// void __attribute__((destructor)) dtor() { printf("%lx", res); }
//N0-d3Bug
