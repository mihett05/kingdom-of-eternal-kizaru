from client.Game import Game
from time import sleep


if __name__ == '__main__':
    while True:
        try:
            game = Game()
            game.run()
        except OSError:
            print("Problem with network")
            print("Restart...")
            sleep(0.5)  # Problem with system network
        else:
            break
