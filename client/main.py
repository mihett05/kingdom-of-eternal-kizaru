from client.Game import Game


if __name__ == '__main__':
    # ex_hook = sys.excepthook
    #
    # def hook(extype, value, traceback):
    #     print(extype, value, traceback)
    #     ex_hook(extype, value, traceback)
    #     sys.exit(1)
    #
    # sys.excepthook = hook

    game = Game()
    game.run()
