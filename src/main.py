from othello import OthelloGame

def main():
    game = OthelloGame()
    # game.show()
    # while not game.winner:
    #     # game.turn()
    #     game.show()
    game.turn("X")
    game.show()
if __name__ == "__main__": 
    main()

