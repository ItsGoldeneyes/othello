
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
        
        return (int(second.group()), int(first.group()))
        
        
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
        self.directions = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']
        self.board = [[0 for __ in range(size)] for _ in range(size)]
        
        self.board[size//2][size//2] = 1
        self.board[(size//2)-1][(size//2)-1] = 1
        self.board[(size//2)-1][size//2] = 2
        self.board[size//2][(size//2)-1] = 2
    
    
    def __str__(self):
        return_val = ""
        add_val = ""
        for line in self.board[::-1]:
            for square in line:
                if square == 0:
                    add_val = '\u2218'
                elif square == 1: 
                    add_val = '\u2B24'
                elif square == 2: 
                    add_val = '\u25EF'
                else:
                    add_val = str(square)
                    
                return_val += " " + add_val
            return_val += "\n"
            
        return return_val
    
        
    def adjacent_spaces(self, pos, directional=False):        
        n = pos[1]+1 < len(self.board)
        s = pos[1]-1 >= 0
        e = pos[0]+1 < len(self.board)
        w = pos[0]-1 >= 0
        
        if directional:
            adjacent = {}
            if n:
                adjacent["n"]= (pos[0], pos[1]+1)
                if e:
                    adjacent["ne"] = (pos[0]+1, pos[1]+1)
                if w:
                    adjacent["nw"] = (pos[0]-1, pos[1]+1)
            if s:
                adjacent["s"]= (pos[0], pos[1]-1)
                if e:
                    adjacent["se"] = (pos[0]+1, pos[1]-1)
                if w:
                    adjacent["sw"] = (pos[0]-1, pos[1]-1)
            if e:
                adjacent["e"]= (pos[0]+1, pos[1])
            if w:
                adjacent["w"]= (pos[0]-1, pos[1])

        else:
            adjacent = []
            if n:
                adjacent.append((pos[0], pos[1]+1))
                if e:
                    adjacent.append((pos[0]+1, pos[1]+1))
                if w:
                    adjacent.append((pos[0]-1, pos[1]+1))
            if s:
                adjacent.append((pos[0], pos[1]-1))
                if e:
                    adjacent.append((pos[0]+1, pos[1]-1))
                if w:
                    adjacent.append((pos[0]-1, pos[1]-1))
            if e:
                adjacent.append((pos[0]+1, pos[1]))
            if w:
                adjacent.append((pos[0]-1, pos[1]))
                
        return adjacent
            
        
    def check_move(self, player, move):
        if move[0] > 7 or move[0] < 0:
            print("X is out of bounds")
            return False
        if move[1] > 7 or move[1] < 0:
            print("Y is out of bounds")
            return False
        
        if self.board[move[0]][move[1]] != 0:
            print("space is taken")
            return False
        
        captures_enemy = False
        adjacent = self.adjacent_spaces(move, directional=True)
        
        for direction in self.directions:
            if self.floodfill(adjacent[direction], player, direction):            
                captures_enemy = True
                break
        
        if not captures_enemy:
            print("Not capturing enemy")
            return False
            
        return True
    
    
    def floodfill(self, move, player, direction, count=0, test=False):
        '''
        Recursive directional floodfill
        Starts at source move, checks adjacent spaces in direction until a friendly space is found
        Returns a list of enemy spaces between source and friendly space
        '''
        if test:
            print('\n')
            print(direction)
            print(move)
            print(self.board[move[0]][move[1]])
            print('count: ', count)
        
        if self.board[move[0]][move[1]] == 0:
            return False
        
        if self.board[move[0]][move[1]] == player and count > 0:
            return True
        
        if self.board[move[0]][move[1]] == (player%2)+1:
            adjacent = self.adjacent_spaces(move, directional=True)
            count += 1
            next_space = self.floodfill(adjacent[direction], player, direction, count)
            
            if next_space:
                if type(next_space) == list:
                    return [move].extend(next_space)
                return [move]
            else:
                return False
        
        return False
            
    
    def move(self, player, move):
        assert type(move) == tuple and len(move) == 2, "Position must be tuple of length 2"
        assert 0 <= move[0] <= 7, "X position out of bounds (0<x<7)"
        assert 0 <= move[1] <= 7, "Y position out of bounds (0<x<7)"
        
        self.board[move[0]][move[1]] = player
        
        adjacent = self.adjacent_spaces(move, directional=True)
        flipped = []
        
        for direction in self.directions:
            potential_flipped = self.floodfill(adjacent[direction], player, direction)
            if potential_flipped:
                flipped.extend(potential_flipped)
                
        for space in flipped:
            self.board[space[0]][space[1]] = player