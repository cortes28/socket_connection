Bryan Cortes - cortes28@csu.fullerton.edu/fernanbryan28@gmail.com
Github - cortes28
Programming language: Python

Note: This program was developed in Ubuntu, which is a Linux distribution. 

How to launch program: 

Start with the server.py file, the <PORT> can be a valid number for port. 

    $--------------------------------------------------------------$
    Server command to launch: 

    python3 server.py <PORT>

    An example of a command that would promptly launch the server: 

    python3 server.py 9999

    $--------------------------------------------------------------$
    Client command to launch:

    python3 client.py <SERVER MACHINE> <PORT>

    An example of a command that would promptly launch the client with the same port number as the
    server (Note that server.py will have to be running already to connect):


    python3 client.py localhost 9999

    $--------------------------------------------------------------$

- If a no port number is given, it will default to 9999
- Has a couple of safety mechanisms such as if the command given was not valid. If such command
    that is not valid is given within the client, it won't send anything to the server.


Once the connection has been established, the client program will prompt the  user with 'ftp>' with the following available commands:

    $--------------------------------------------------------------$
    ftp> get <FILE NAME> -> downloads file <FILE NAME> from the server.
    ftp> put <FILE NAME> -> uploads the file <FILE NAME> to the server.
    ftp> ls -> lists the files on the server
    ftp> quit -> disconnects the client from the server.

    An example for get/put would be as follows:

    ftp> get file.txt

    $--------------------------------------------------------------$


Quitting the connection from the client will display the total amount of bytes transferred. 