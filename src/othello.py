import logging
import re

class OthelloGame():
    def __init__(self, debug=False):
        self.board = OthelloBoard(debug=debug)
        self.winner = False
        self.stalemate_timer = 0
        self.debug = debug


    def show(self):
        print(self.board)


    def extract_pos(self, pos_str):
        '''
        Get position from input using regex
        '''
        
        first = re.search(r"\d", pos_str)
        if first == None:
            raise ValueError("Input contains no numbers")
        
        second = re.search(r"\d+", pos_str[first.start()+1:])
        if second == None:
            raise ValueError("Input contains only one number")
        
        return (int(first.group()), int(second.group()))
    
    
    def get_info(self):
        '''
        Returns information about the game for NEAT to use
        '''
        output = []
        for line in self.board.get_board():
            for space in line:
                output.append(space)
                
        print(output)
        return output
        
        
    def turn(self, player, pos= False):
        '''
        Takes a turn for a given player
        If pos is given, it will attempt to move there, otherwise it will ask for input
        '''
        assert player == 1 or player == 2
        
        if self.board.check_stalemate(player):
            self.stalemate_timer += 1
            
            if self.stalemate_timer >= 2:
                self.winner = True
                if self.debug:
                    print("Game is a stalemate!")
                
            return True
        
        # If not stalemate, reset timer
        self.stalemate_timer = 0
        
        if pos:
            if not self.board.check_move(player, pos):
                return False
            else:
                self.board.move(player, pos)
                
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
            
        if self.board.check_winner():
            if type(self.board.check_winner()) == int:
                if self.debug:
                    print(f'\nPlayer {self.board.winner} has won!')
                self.winner = self.board.winner
            else:
                self.winner = True
                if self.debug:
                    print('Game is a draw!')
                    
        if self.debug:
            self.show()
                
            
        return True
    
    
class OthelloBoard():
    def __init__(self, size=8, debug=False):
        self.board = [[0 for __ in range(size)] for _ in range(size)]
        self.winner = False
        self.debug = debug
        
        self.board[size//2][size//2] = 1
        self.board[(size//2)-1][(size//2)-1] = 1
        self.board[(size//2)-1][size//2] = 2
        self.board[size//2][(size//2)-1] = 2
        
    
    def __str__(self):
        '''
        Returns a formatted string representation of the board for printing
        '''
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
    
    
    def get_board(self):
        return self.board
    
    
    def adjacent_spaces(self, pos, directional=False):
        '''
        Returns a list of adjacent spaces to a given position
        If directional is True, returns a dictionary of adjacent spaces with their direction
        '''
        n = pos[0]+1 < len(self.board)
        s = pos[0]-1 >= 0
        e = pos[1]+1 < len(self.board)
        w = pos[1]-1 >= 0
        
        if directional:
            adjacent = {}
            if n:
                adjacent["n"]= (pos[0]+1, pos[1])
                if e:
                    adjacent["ne"] = (pos[0]+1, pos[1]+1)
                if w:
                    adjacent["nw"] = (pos[0]+1, pos[1]-1)
            if s:
                adjacent["s"]= (pos[0]-1, pos[1])
                if e:
                    adjacent["se"] = (pos[0]-1, pos[1]+1)
                if w:
                    adjacent["sw"] = (pos[0]-1, pos[1]-1)
            if e:
                adjacent["e"]= (pos[0], pos[1]+1)
            if w:
                adjacent["w"]= (pos[0], pos[1]-1)

        else:
            adjacent = []
            if n:
                adjacent.append((pos[0]+1, pos[1]))
                if e:
                    adjacent.append((pos[0]+1, pos[1]+1))
                if w:
                    adjacent.append((pos[0]+1, pos[1]-1))
            if s:
                adjacent.append((pos[0]-1, pos[1]))
                if e:
                    adjacent.append((pos[0]-1, pos[1]+1))
                if w:
                    adjacent.append((pos[0]-1, pos[1]-1))
            if e:
                adjacent.append((pos[0], pos[1]+1))
            if w:
                adjacent.append((pos[0], pos[1]-1))
                
        return adjacent
    
    
    def floodfill(self, move, player, direction, count=0, test=False):
        '''
        Recursive directional floodfill
        Starts at source move, checks adjacent spaces in direction until a friendly space is found
        Returns a list of enemy spaces between source and friendly space
        '''
        if test:
            print('\n')
            print("direction: ", direction)
            print(move,self.board[move[0]][move[1]])
            print('count: ', count)
            print('enemy space?',self.board[move[0]][move[1]] == (player%2)+1)
        
        if self.board[move[0]][move[1]] == 0:
            return False
        
        if self.board[move[0]][move[1]] == player and count > 0:
            return True
        
        if self.board[move[0]][move[1]] != (player%2)+1:
            return False
        
        adjacent = self.adjacent_spaces(move, directional=True)
        
        if direction not in adjacent:
            # Out of bounds
            return False
        
        count += 1
        return_val = [move]
        next_space = self.floodfill(adjacent[direction], player, direction, count)
        
        if not next_space:
            return False
        
        if type(next_space) == list:
            return_val.extend(next_space)
        return return_val        
        
        
    def count_pieces(self, player):
        '''
        Returns the number of pieces a player has on the board
        '''
        count = 0
        for line in self.board:
            for square in line:
                if square == player:
                    count += 1
        return count
    
        
    def get_possible_moves(self, player):
        '''
        Check floodfill spaces of all possible moves
        Can filter by edge pieces if inefficient
        '''
        
        possible_moves = []
        for x in range(len(self.board)):
            for y in range(len(self.board)):
                self.debug = False
                if self.check_move(player, (x,y)):
                    possible_moves.append((x,y))
                self.debug = True
        return possible_moves
    
    
    def check_move(self, player, move):
        '''
        Check if a move is valid
        Returns True if valid, False if invalid
        '''
        if move[0] > 7 or move[0] < 0:
            if self.debug:
                print("X is out of bounds")
            return False
        if move[1] > 7 or move[1] < 0:
            if self.debug:
                print("Y is out of bounds")
            return False
        
        if self.board[move[0]][move[1]] != 0:
            if self.debug:
                print("space is taken")
            return False
        
        captures_enemy = False
        adjacent = self.adjacent_spaces(move, directional=True)
        for direction in adjacent:
            if self.floodfill(adjacent[direction], player, direction):            
                captures_enemy = True
                break
        
        if not captures_enemy:
            if self.debug:
                print("Not capturing enemy")
            return False
            
        return True
    
    
    def check_winner(self):
        '''
        Checks if there are any empty spaces, if not, checks the number of pieces each player has
        Returns the winner, or True if it's a draw
        '''
        if any(0 in row for row in self.board):
            return False
        
        player_1_count = sum(row.count(1) for row in self.board)
        player_2_count = sum(row.count(2) for row in self.board)
        
        if player_1_count > player_2_count:
            self.winner = 1
            return 1
        elif player_2_count > player_1_count:
            self.winner = 2
            return 2
        else:
            self.winner = True
            return True
        
    
    def check_stalemate(self, player):
        '''
        Checks possible moves of player and returns True if none are available
        '''
        player_moves = self.get_possible_moves(player)
        
        if len(player_moves) > 0:
            return False
        
        return True
    
    
    def move(self, player, move):
        '''
        Puts player piece on move, captures enemy pieces
        '''
        assert type(move) == tuple and len(move) == 2, "Position must be tuple of length 2"
        assert 0 <= move[0] <= 7, "X position out of bounds (0<x<7)"
        assert 0 <= move[1] <= 7, "Y position out of bounds (0<x<7)"
        
        self.board[move[0]][move[1]] = player
        
        adjacent = self.adjacent_spaces(move, directional=True)
        flipped = []
        
        for direction in adjacent:
            potential_flipped = self.floodfill(adjacent[direction], player, direction)
            if potential_flipped:
                flipped.extend(potential_flipped)
                
        for space in flipped:
            self.board[space[0]][space[1]] = player