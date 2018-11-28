#!/usr/bin/env python3

import socket
import sys
import os
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", help="server IP address", default="localhost")
    parser.add_argument("-p", type=int, help="server port", default=10000)
    args = parser.parse_args()

    try:
        player_name = input("Type your name: ")

        while True:
            # New Game Solicitation
            s = socket.socket()
            s.connect((args.a, args.p))

            # Wait for Game Start
            print("Waiting for an opponent...")
            data_recv = s.recv(128)
            print(data_recv.decode())

            # Send player's name
            s.send(player_name.encode())

            # Turn
            print("Your turn!")
            player_choice = ""
            while (player_choice not in ["r", "p", "s"]):
                player_choice = input(
                    "Enter 'r' for Rock, 'p' for Paper or 's' for Scissor: ")

            s.send(player_choice.encode())

            print("Waiting for the opponent's turn...")

            # Opponent's choice
            opponent_choice = s.recv(1).decode()

            # Result
            s.settimeout(0.2)
            result = s.recv(32)
            s.settimeout(None)

            # Print ASCII image
            case = player_choice + "_vs_" + opponent_choice
            print_image(case)

            # Print result
            print(result.decode())

            # Play again
            s.close()
            print(
                "Do you want to play again? Press \'Enter\' for \'Yes\' or type anything for \'No\'")
            if input() == "":
                continue
            else:
                print("Game finished")
                return
    except Exception:
        return


def print_image(case):
    with open("ascii_images/" + case + ".txt", "r") as f:
        print(f.read())


if __name__ == '__main__':
    main()
