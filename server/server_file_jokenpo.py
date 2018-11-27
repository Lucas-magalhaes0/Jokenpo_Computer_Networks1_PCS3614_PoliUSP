#!/usr/bin/env python3

import socket
import sys
import os
import threading
import time
import argparse
from player import Player


def send_draw(player1, player2):
    player1.conn.send("Draw :|".encode())
    player2.conn.send("Draw :|".encode())


def send_player1_wins(player1, player2):
    player1.conn.send("You Win! :)".encode())
    player2.conn.send("You Lose :(".encode())


def send_player2_wins(player1, player2):
    player1.conn.send("You Lose :(".encode())
    player2.conn.send("You Win! :)".encode())


def send_operation_invalid(player1, player2):
    player1.conn.send("Invalid operation".encode())
    player2.conn.send("Invalid operation".encode())


def get_winner(player1_choice, player2_choice):

    # Draw
    if player1_choice == player2_choice:
        return 0

    if player1_choice == "r":
        if player2_choice == "s":
            return 1
        if player2_choice == "p":
            return 2

    if player1_choice == "p":
        if player2_choice == "r":
            return 1
        if player2_choice == "s":
            return 2

    if player1_choice == "s":
        if player2_choice == "p":
            return 1
        if player2_choice == "r":
            return 2

    # Invalid operation
    return 3


class GameThread (threading.Thread):
    def __init__(self, player1, player2):
        threading.Thread.__init__(self)

        self.player1 = player1
        self.player2 = player2

    def run(self):
        try:
            welcome_message = "\n" + \
                "---------------------\n" + \
                "Welcome to JoKenPo!\n" + \
                "   Game Started\n" + \
                "---------------------\n"

            # Send welcome message
            self.player1.conn.send(welcome_message.encode())
            self.player2.conn.send(welcome_message.encode())

            # Timeout for receiving names
            self.player1.conn.settimeout(0.3)
            self.player2.conn.settimeout(0.3)

            # Wait for players names
            self.player1.name = self.player1.conn.recv(200).decode()
            self.player2.name = self.player2.conn.recv(200).decode()

            # Return to blocking mode.
            self.player1.conn.settimeout(None)
            self.player2.conn.settimeout(None)

            # Wait for players turns
            self.player1.choice = self.player1.conn.recv(1).decode()
            self.player2.choice = self.player2.conn.recv(1).decode()

            print(self.player1.name + "'s choice: " + self.player1.choice)
            print(self.player2.name + "'s choice: " + self.player2.choice)

            # Send opponent's choice
            self.player1.conn.send(self.player2.choice.encode())
            self.player2.conn.send(self.player1.choice.encode())

            # Result calculation and messages

            send_result = [
                send_draw,
                send_player1_wins,
                send_player2_wins,
                send_operation_invalid,
            ]

            send_result[get_winner(self.player1.choice, self.player2.choice)](
                self.player1, self.player2)

        finally:
            self.player1.conn.close()
            self.player2.conn.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", help="server IP address", default="localhost")
    parser.add_argument("-p", type=int, help="server port", default=10000)
    args = parser.parse_args()

    print("Waiting connections")
    try:
        s = socket.socket()
        s.bind((args.a, args.p))
        s.listen(10)
        next_id = 1
        while True:
            conn, address = s.accept()
            player1 = Player(next_id, "Player 1", conn, address)
            print("Connected with player 1: " + str(address))
            next_id = next_id + 1

            conn, address = s.accept()
            player2 = Player(next_id, "Player 2", conn, address)
            print("Connected with player 2: " + str(address))
            next_id = next_id + 1

            gt = GameThread(player1, player2)
            gt.start()

    except Exception as e:
        print(e)
        return


if __name__ == '__main__':
    main()
