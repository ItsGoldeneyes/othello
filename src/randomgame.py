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
        print('Player', player, end=': ')
        while not game.turn(player, move):
            
            print(move, end=' ')
            time.sleep(0.05)
            
            move = (random.randint(0,7), random.randint(0,7))
            tried_moves.append(move)
            
            while move in moves_done:
                tried_moves.append(move)
                while move in tried_moves:
                    move = (random.randint(0,7), random.randint(0,7))
        
        moves_done.append(move)
        print('\n', end='')
        game.show()
        time.sleep(0.5)
        player = (player%2)+1
if __name__ == "__main__": 
    main()