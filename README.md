# Multithreaded socket JoKenPo

This is a paper for the subject of Computer Networks I - PCS3614 of the Polytechnic School of the University of São Paulo (USP).

It involves the use of sockets in Python to integrate clients through a local server, using threads.

In this work, the server will control the game module, implementing logic and clients will be able to connect to it and play on different threads, two by two.

## Instructions

In order to run the game, you must run the server first. To do that, open a terminal window, go to directory [server](server) and run:

> ./server_file_jokenpo.py

Then, you must run two clients (one for each player). To do that, open two terminal windows and, in both of them, go to directory [client](client) and run:

> ./client_file_jokenpo.py

It is also possible to change the IP address and port used in the socket. For the server, this can be done by running:

> ./server_file_jokenpo.py -a ip_address -p port

For the client, this can be done by running:

> ./client_file_jokenpo.py -a ip_address -p port

Replace  `ip_address` for the IP address you want to use and `port` for the port you want to use.

By default, `ip_address` is `localhost` and `port` is `10000`.

The IP address and port must be the same for the server and the clients.
