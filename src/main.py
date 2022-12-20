from othello import OthelloGame
import numpy as np
import othello_minimax as om
import random
import pickle
import time
import os


class Othello:
    def __init__(self):
        self.game = OthelloGame()
        
    def play(self):
        self.game.reset()
        player = 1
        self.game.show()
        
        while not self.game.winner:
            self.game.turn(player)
            self.game.show()
            player = (player%2)+1
            
        return self.game.winner()
    
    def play_minimax(self):
        self.game.reset()
        player = 1
        self.game.show()
        mm = om.Minimax()
        
        while not self.game.winner:
            if player == 1:
                self.game.turn(player)
                self.game.show()
            else:
                move = mm.move(self.game.board)
                self.game.turn(move)
                
            player = (player%2)+1
            
        return self.game.winner()
    

if __name__ == "__main__":
    game = Othello()
    
    game.play()