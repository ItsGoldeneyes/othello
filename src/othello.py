
import re

class OthelloGame():
    def __init__(self):
        self.winner = False
        self.board = OthelloBoard()
     
        
    def show(self):
        print(self.board)
    
    
    def extract_pos(self, pos_str):
        '''
        Get position from input + flip so orients correctly
        '''
        
        first = re.search(r"\d", pos_str)
        if first == None:
            raise ValueError("Input contains no numbers")
        
        second = re.search(r"\d+", pos_str[first.start()+1:])
        if second == None:
            raise ValueError("Input contains only one number")
        
        return (int(second.group())-1, int(first.group())-1)
        
        
    def turn(self, player, pos= False):
        assert player == 1 or player == 2
        
        if pos:
            if not self.board.check_move(player, pos):
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
                    valid = self.board.check_move(player, pos_tuple)
                    
            self.board.move(player, pos_tuple)
                
    
    
class OthelloBoard():
    def __init__(self, size=8):
        self.board = [[0 for __ in range(size)] for _ in range(size)]
        
        self.board[size//2][size//2] = 1
        self.board[(size//2)-1][(size//2)-1] = 1
        self.board[(size//2)-1][size//2] = 2
        self.board[size//2][(size//2)-1] = 2
    
        
    def move(self, player, pos):
        assert type(pos) == tuple and len(pos) == 2, "Position must be tuple of length 2"
        assert 0 <= pos[0] <= 7, "X position out of bounds (0<x<7)"
        assert 0 <= pos[1] <= 7, "Y position out of bounds (0<x<7)"
        
        self.board[pos[0]][pos[1]] = player+1
        
        
    def check_move(self, player, move):
        print(move)
        if move[0] > 7 or move[0] < 0:
            print("X is out of bounds")
            return False
        if move[1] > 7 or move[1] < 0:
            print("Y is out of bounds")
            return False
        
        if self.board[move[0]][move[1]] != 0:
            print("space is taken")
            return False
        
        adjacent_to_enemy = False
        
        if move[0] <= len(self.board[0]):
            if self.board[move[0]+1][move[1]] == ((player+1)%2)+1:
                adjacent_to_enemy = True
                
        if move[1] <= len(self.board[0]):
            if self.board[move[0]][move[1]+1] == ((player+1)%2)+1:
                adjacent_to_enemy = True
                
        if move[0] >= 0:
            if self.board[move[0]-1][move[1]] == ((player+1)%2)+1:
                adjacent_to_enemy = True
                
        if move[1] >= 0:
            if self.board[move[0]][move[1]-1] == ((player+1)%2)+1:
                adjacent_to_enemy = True
        
        if not adjacent_to_enemy:
            print("Not adjacent to enemy")
            return False
            
        return True
        
    def __str__(self):
        return_val = ""
        add_val = ""
        for line in self.board[::-1]:
            for square in line:
                if square == 0:
                    add_val = '\u2218'
                elif square%2 == 1: 
                    add_val = '\u25EF'
                elif square%2 == 0: 
                    add_val = '\u2B24'
                    
                return_val += " " + add_val
            return_val += "\n"
            
        return return_val