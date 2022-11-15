
import re

class OthelloGame():
    def __init__(self):
        self.winner = False
        self.board = OthelloBoard()
     
        
    def show(self):
        print(self.board)
    
    
    def extract_pos(self, pos_str):
        first = re.search(r"\d", pos_str)
        if first == None:
            raise ValueError("Input contains no numbers")
        
        second = re.search(r"\d+", pos_str[first.start()+1:])
        if second == None:
            raise ValueError("Input contains only one number")
        
        return (int(first.group()), int(second.group()))
    
    
    def check_move(self, player, move):
        return True
        
        
    def turn(self, player, pos= False):
        if pos:
            if not self.check_move(player, pos):
                return False
            else:
                self.board.move(player, pos)
            # Logic to check move
            # return True
        else:
            valid = False
            while not valid:
                pos_input = input(f"Where would player {player} like to move?")
                pos_tuple = False
                
                try: 
                    pos_tuple = self.extract_pos(pos_input)
                except ValueError as e:
                    print(e)
                    
                if pos_tuple:
                    valid = self.check_move(player, pos_tuple)
                    
            self.board.move(player, pos_tuple)
                
    
    
class OthelloBoard():
    def __init__(self):
        self.board = [[0 for i in range(8)] for j in range(8)]
        
    def move(self, player, pos):
        assert player == "X" or player == "O", "Player must be either X or O"
        assert type(pos) == tuple and len(pos) == 2, "Position must be tuple of length 2"
        assert 0 <= pos[0] <= 7, "X position out of bounds (0<x<7)"
        assert 0 <= pos[1] <= 7, "Y position out of bounds (0<x<7)"
        
        self.board[pos[0]][pos[1]] = player
        
    def __str__(self):
        return_val = ""
        for line in self.board:
            for square in line:
                return_val += " " + str(square)
            return_val += "\n"
            
        return return_val