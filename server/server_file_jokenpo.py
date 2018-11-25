import socket
import sys
import os
from thread import *

s = socket.socket()
s.bind(("localhost",9996))
s.listen(2) # Acepta hasta 2 conexiones entrantes.


def main():
    f = open ("jokenpo", "a")
    print "Waiting connections"
    try:
        while True:
            (conn, address) = s.accept()

            player1 = str(address)
            f.write("Player 1" + player1 + "\n")
            print "Connected with player1: " + str(address)

            (conn2, address2) = s.accept()
            
            player2 = str(address2)
            f.write("Player 2" + player2 + "\n")
            print "Connected with player2: " + str(address2)

            start_new_thread(game_thread, (conn, address, conn2, address2))
    except Exception as e:
        print e.message
        return 
    
        
def game_thread(conn, address, conn2, address2):
    try:
        # Welcome message
        conn.send("\n---------------------\nWelcome to JoKenPo! \n   Game Started\n---------------------\n")
        conn2.send("\n---------------------\nWelcome to JoKenPo! \n   Game Started\n---------------------\n")

        # Wait for players turn
        player1 = conn.recv(1)
        player2 = conn2.recv(1)
        

        print "Player1's choice " + player1
        print "Player2's choice " + player2

        # result calculation
        case = ""
        case2 = ""
        player1_wins = False
        player2_wins = False
        if (player1 == "p" ):
            if (player2 =="r"):
                player1_wins = True
                player2_wins = False
                case = "p_vs_r"
                case2 = "r_vs_p"
            if (player2 =="s"):
                player1_wins = False
                player2_wins = True
                case = "p_vs_s"
                case2 = "s_vs_p"
            if (player2 =="p"):
                player1_wins = False
                player2_wins = False
                case = "p_vs_p"
                case2 = "p_vs_p"
        elif (player1 == "r" ):
            if (player2 =="r"):
                player1_wins = False
                player2_wins = False
                case = "r_vs_r"
                case2 = "r_vs_r"
            if (player2 =="s"):
                player1_wins = True
                player2_wins = False
                case = "r_vs_s"
                case2 = "s_vs_r"
            if (player2 =="p"):
                player1_wins = False
                player2_wins = True
                case = "r_vs_p"
                case2 = "p_vs_r"
        else:
            if (player2 =="r"):
                player1_wins = False
                player2_wins = True
                case = "s_vs_r"
                case2 = "r_vs_s"
            if (player2 =="s"):
                player1_wins = False
                player2_wins = False
                case = "s_vs_s"
                case2 = "s_vs_s"
            if (player2 =="p"):
                player1_wins = True
                player2_wins = False
                case = "s_vs_p"
                case2 = "p_vs_s"

        
        #result messages
        if (player1_wins and not(player2_wins)):
            conn.send(case)
            conn2.send(case2)
            conn.send("You Win! :)")
            conn2.send("You Lose :(")
        elif (not(player1_wins) and player2_wins):
            conn.send(case)
            conn2.send(case2)
            conn.send("\nYou Lose :(")
            conn2.send("\nYou Win! :)")
        else:
            conn.send(case)
            conn2.send(case2)
            conn.send("Draw :|")
            conn2.send("Draw :|")
        
    except Exception as e:
        conn.close()
        conn2.close()
        return


if __name__ == '__main__':
    main()

