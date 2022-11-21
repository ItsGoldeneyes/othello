from othello import OthelloGame

def main():
    game = OthelloGame()
    game.show()
    player = 0
    while not game.winner:
        game.turn(player+1)
        game.show()
        
        player = (player + 1)%2
    
    
if __name__ == "__main__": 
    main()