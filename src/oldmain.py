from othello.othello import OthelloGame

def main():
    game = OthelloGame()
    game.show()
    player = 1
    
    while not game.winner:
        game.turn(player)
        info = game.get_info()
        game.show()
        
        player = (player%2)+1
    

if __name__ == "__main__": 
    main()