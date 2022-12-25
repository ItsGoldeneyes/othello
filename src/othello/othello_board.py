
class OthelloBoard():
    
    def __init__(self, size=8, debug=False, board=False):
        if board:
            self.board = board
        else:
            self.board = [[0 for __ in range(size)] for _ in range(size)]
        self.winner = False
        self.debug = debug
        self.flip_count = [0, 0]
        
        
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
    
    
    def copy(self):
        return OthelloBoard(board = [row[:] for row in self.board])
        
    
    def get_flip_count(self, player):
        if player == 1:
            return self.flip_count[0]
        elif player == 2:
            return self.flip_count[1]
               
    
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
    
        
    def get_actual_moves(self, player):
        '''
        Check floodfill spaces of all possible moves
        Actual moves are moves that flip at least one piece
        '''
        self.debug = False
        
        actual_moves = [[(x,y) for y in range(len(self.board)) 
                           if self.check_move((x,y), player)] 
                          for x in range(len(self.board))]
        
        self.debug = True
        return actual_moves
    
    def get_potential_moves(self, player):
        '''
        Check spaces with adjacent empty space
        Potential spaces could be contested in the future
        '''
        
    
    def check_flips(self, move, player):
        '''
        Get flips from a given move
        '''
        adjacent = self.adjacent_coords(move, directional=True)
        flips = []
        
        for direction in adjacent:
            potential_flipped = self.floodfill(adjacent[direction], player, direction)
            if potential_flipped:
                flips.extend(potential_flipped)
        
        return flips
    
    
    def check_move(self, move, player):
        '''
        Check if a move is valid
        Returns True if valid, False if invalid
        '''
        if move[0] > 7 or move[0] < 0:
            # if self.debug:
            #     print("X is out of bounds")
            return False
        if move[1] > 7 or move[1] < 0:
            # if self.debug:
            #     print("Y is out of bounds")
            return False
        
        if self.board[move[0]][move[1]] != 0:
            # if self.debug:
            #     print("space is taken")
            return False
        
        captures_enemy = False
        adjacent = self.adjacent_coords(move, directional=True)
        for direction in adjacent:
            if self.floodfill(adjacent[direction], player, direction):            
                captures_enemy = True
                break
        
        if not captures_enemy:
            # if self.debug:
            #     print("Not capturing enemy")
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
        player_moves = self.get_actual_moves(player)
        if len(player_moves) > 0:
            return False
        
        return True
    
    def adjacent_coords(self, pos, direction=False, directional=False):
        '''
        Returns a list of adjacent spaces to a given position
        If directional is True, returns a dictionary of adjacent spaces with their direction
        '''
        n = pos[0]+1 < len(self.board)
        s = pos[0]-1 >= 0
        e = pos[1]+1 < len(self.board)
        w = pos[1]-1 >= 0
        
        if direction:
            if n:
                if e:
                    return (pos[0]+1, pos[1]+1)
                if w:
                    return (pos[0]+1, pos[1]-1)
                return (pos[0]+1, pos[1])
            if s:
                if e:
                    return (pos[0]-1, pos[1]+1)
                if w:
                    return (pos[0]-1, pos[1]-1)
                return (pos[0]-1, pos[1])
            if e:
                return (pos[0], pos[1]+1)
            if w:
                return (pos[0], pos[1]-1)
            return False
        
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
    
    def adjacent_spaces(self, pos, direction=False, directional=False):
        '''
        Returns a list of adjacent spaces to a given position
        If directional is True, returns a dictionary of adjacent spaces with their direction
        '''
        n = pos[0]+1 < len(self.board)
        s = pos[0]-1 >= 0
        e = pos[1]+1 < len(self.board)
        w = pos[1]-1 >= 0
        
        if direction:
            if n:
                if e:
                    return self.board[pos[0]+1, pos[1]+1]
                if w:
                    return self.board[pos[0]+1, pos[1]-1]
                return self.board[pos[0]+1, pos[1]]
            if s:
                if e:
                    return self.board[pos[0]-1, pos[1]+1]
                if w:
                    return self.board[pos[0]-1, pos[1]-1]
                return self.board[pos[0]-1, pos[1]]
            if e:
                return self.board[pos[0], pos[1]+1]
            if w:
                return self.board[pos[0], pos[1]-1]
        
        if directional:
            adjacent = {}
            if n:
                adjacent["n"]= self.board[pos[0]+1, pos[1]]
                if e:
                    adjacent["ne"] = self.board[pos[0]+1, pos[1]+1]
                if w:
                    adjacent["nw"] = self.board[pos[0]+1, pos[1]-1]
            if s:
                adjacent["s"]= self.board[pos[0]-1, pos[1]]
                if e:
                    adjacent["se"] = self.board[pos[0]-1, pos[1]+1]
                if w:
                    adjacent["sw"] = self.board[pos[0]-1, pos[1]-1]
            if e:
                adjacent["e"]= self.board[pos[0], pos[1]+1]
            if w:
                adjacent["w"]= self.board[pos[0], pos[1]-1]

        else:
            adjacent = []
            if n:
                adjacent.append(self.board[pos[0]+1, pos[1]])
                if e:
                    adjacent.append(self.board[pos[0]+1, pos[1]+1])
                if w:
                    adjacent.append(self.board[pos[0]+1, pos[1]-1])
            if s:
                adjacent.append(self.board[pos[0]-1, pos[1]])
                if e:
                    adjacent.append(self.board[pos[0]-1, pos[1]+1])
                if w:
                    adjacent.append(self.board[pos[0]-1, pos[1]-1])
            if e:
                adjacent.append(self.board[pos[0], pos[1]+1])
            if w:
                adjacent.append(self.board[pos[0], pos[1]-1])
                
        return adjacent
    
    def safe_pieces(self, player):
        '''
        Returns a list of pieces that are safe from capture
        
        TODO: Edge detection, area control
        '''
        safe_pieces = []
        for x in range(len(self.board)):
            for y in range(len(self.board)):
                if self.board[x][y] == player:
                    if self.check_move((x,y), player):
                        safe_pieces.append((x,y))
        return safe_pieces
    
    
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
        
        adjacent = self.adjacent_coords(move, directional=True)
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
    
    
    def undo_move(self, state):
        
        self.board = state[0]
        self.flip_count = state[1]
        
        
    def move(self, move, player):
        '''
        Puts player piece on move, captures enemy pieces
        '''
        assert type(move) == tuple and len(move) == 2, "Position must be tuple of length 2"
        assert 0 <= move[0] <= 7, "X position out of bounds (0<x<7)"
        assert 0 <= move[1] <= 7, "Y position out of bounds (0<x<7)"
        
        state = ([row[:] for row in self.board], [*self.flip_count])
                
        potential_flips = self.check_flips(move, player)
        self.flip_count[player-1] += len(potential_flips)
        self.board[move[0]][move[1]] = player
        
        for space in potential_flips:
            self.board[space[0]][space[1]] = player
            
        
        return state