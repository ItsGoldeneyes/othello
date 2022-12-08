from othello import OthelloGame
import random
import time

def main():
    game = OthelloGame()
    game.show()
    player = 1
    moves_done = [(4,3), (3,4), (4,4), (3,3)]
    move=(0,0)
    while not game.winner:
        tried_moves = []
        while not game.turn(player, move):
            
            print(player, move)
            time.sleep(0.1)
            
            move = (random.randint(0,7), random.randint(0,7))
            tried_moves.append(move)
            
            while move in moves_done:
                tried_moves.append(move)
                while move in tried_moves:
                    move = (random.randint(0,7), random.randint(0,7))
                
                

        
        moves_done.append(move)
        game.show()
        time.sleep(0.5)
        player = (player%2)+1
    
if __name__ == "__main__": 
    main()