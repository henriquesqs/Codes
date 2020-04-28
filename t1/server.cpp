/*
    Establishing a socket to the server side of application.
*/

#include <arpa/inet.h>
#include <iostream>
#include <netdb.h>
#include <netinet/in.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>

using namespace std;

int main(int argc, char const *argv[]) {

    // Creating a sockaddr_in which describes the internet protocol version 4 (ipv4)

    sockaddr_in server_address;
    socklen_t serverSize = sizeof(server_address);
    server_address.sin_family = AF_INET;
    server_address.sin_port = htons(51000);
    inet_pton(AF_INET, "0.0.0.0", &server_address.sin_addr);

    // Creating a socket with IPv4 Internet protocols as communication domain and TCP as communication semantics.
    // AF_INET = IPv4 protocol, SOCK_STREAM = TCP.
    int socket = ::socket(AF_INET, SOCK_STREAM, 0);

    // Checking for errors while creating a socket
    if (socket == -1) {
        cerr << "Can't create a socket.";
        return -1;
    }

    // Binding the created socket 'socket' to an available address 'server_address' of size 'sizeof(server_address)' bytes.
    // This step is commonly named as 'lqassigning a name to a socketrq'.
    if (bind(socket, (sockaddr *)&server_address, serverSize) != 0) {
        cerr << "Can't bind to IP/port.";
        return -2;
    }

    // Listenning for connections by marking 'socket' as a passive connection, i.e., 'a socket
    // that will be used to accept incoming connection requests using accept()' later.
    if (listen(socket, SOMAXCONN) != 0) {
        cerr << "Can't listen to this port.";
        return -3;
    }

    // Accepting connections by extracting the first request on queue.
    // If everything goes right, 'server_address' receives the connecting
    // peer, 'address_length' receives the address' actual length and
    // 'clientSocket' receives socket's descriptor.

    int clientSocket;
    sockaddr_in client;
    char host[NI_MAXHOST];
    char service[NI_MAXSERV];
    socklen_t clientSize = sizeof(client);

    clientSocket = accept(socket, (sockaddr *)&client, &clientSize);

    if (clientSocket == -1) {
        cerr << "Error on connecting to socket.";
        return -4;
    }

    close(socket);

    memset(host, 0, NI_MAXHOST);    // cleaning possible garbage on host
    memset(service, 0, NI_MAXSERV); // cleaning possible garbage on service

    // get computer information
    int info = getnameinfo((sockaddr *)&server_address, serverSize, host, NI_MAXHOST, service, NI_MAXSERV, 0);

    if (info)
        cout << host << " connected on " << service << "\n";
    else {
        inet_ntop(AF_INET, &client.sin_addr, host, NI_MAXHOST);
        cout << host << " connected on port " << ntohs(server_address.sin_port) << "\n";
    }

    char buff[4096];
    int bytesReceived = 0, bigNick = 0;

    char nickname[20];
    char confirmationMsg[14] = "Message sent!";
    char confirmNick[40] = "Your nickname is registered. Have fun!!";
    char welcomeMsg[91] = "Hello, there! Welcome to my TCP server.\nPlease, enter your nickname (max of 20 letters): ";
    string msg;

    send(clientSocket, welcomeMsg, sizeof(welcomeMsg), 0);             // sending welcome message
    bytesReceived = recv(clientSocket, nickname, sizeof(nickname), 0); // waiting for user to input his nickname

    send(clientSocket, confirmNick, sizeof(confirmNick), 0); // sending confirmation of nickname
    string(nickname, 0, bytesReceived);                      // storing client's nickname

    cout << "Client's nickname: " << nickname << "\n\n"
         << "Start of the conversation:\n\n";

    while (true) {

        //limpando msg pra poder mostrar certinho dps
        msg.erase(0, msg.size());

        memset(buff, 0, 4096); // cleaning the buffer
        bytesReceived = 0;

        // send(clientSocket, confirmationMsg, sizeof(confirmationMsg), 0); // asking for a message
              
        bytesReceived = recv(clientSocket, buff, 4096, 0);               // waiting for a message

        // checking for any errors
        if (bytesReceived == -1) {
            cerr << "Error on receiving message. Stopping."
                 << "\n";
            break;
        }

        if (bytesReceived == 0) {
            cout << "Client disconnected. Stopping."
                 << "\n";
            break;
        }

        send(clientSocket, buff, 4096, 0); // ressend message

        /* caso a mensagem tenha menos do que 4096 caracteres, ou seja o que restou da mensagem com mais de 4096 caracteres, 
        ela é colocada no buffer e enviada ao cliente */
        buff[4095] = 0;
        msg = buff;

        cout << "Message from " << nickname << " : " << msg << "\n"; // display message
    }

    close(clientSocket);

    return 1;
}