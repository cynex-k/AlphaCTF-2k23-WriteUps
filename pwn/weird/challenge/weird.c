#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void disable_buffering(){
    setbuf(stdin,NULL);
    setbuf(stdout,NULL);
    setbuf(stderr,NULL);

}

int main()
{

    char str[100];
    int num = 0, num2 = 2000;
    int sum = 0;
    int sign = 1;
    char input[50];
    float value;
    disable_buffering();
    printf("Hello Hacker here is a easy one can you make it leet:\n");
    fgets(str, 100, stdin);
    if (str[0] == '-')
    {
        sign = -1;
    }
    num = atoi(str);
    if (sign == -1)
    {
        num = -num;
    }
    // num  =4294966633
    sum = num2 + num;
    if (sum == 1337)
    {

        printf("Good job this one is easier all you have to do is find the solution: ");
        fgets(input, 50, stdin);
        value = strtof(input, NULL);
        if (value < 36.35928345)
        {
            printf("This is Low!!!!!\n");
            exit(0);
        }
        else if (value > 36.35928345)
        {
            printf("This is High!!!!!\n");
            exit(0);
        }
        else
        {
            FILE *fp = fopen("flag.txt", "r");
            if (fp == NULL)
            {
                printf("Error: unable to open file.\n");
                exit(0);
            }

            char buffer[50];
            while (fgets(buffer, 50, fp) != NULL)
            {
                printf("%s", buffer);
            }

            fclose(fp);
        }

        return 0;
    }
    else
    {
        puts("Nah");
        return 0;
    }
    return 0;
}

