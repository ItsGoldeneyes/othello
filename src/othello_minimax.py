import math


class Minimax:
    
    def __init__(self):
        pass
    
    
    def move(self, board, player):
        self.board = board
        self.player = player
        
        best_move = [(0, 0), -(math.inf)]
        for move in board.get_actual_moves(player):
            _, val = self.minimax(board, player, depth=3)
            
            if val > best_move[1]:
                best_move = [move, val]
        return best_move[0]
    

    def evaluate_piece_count(self, board):
        piece_count = board.count_pieces(self.player)
        opp_piece_count = board.count_pieces((self.player%2)+1)
        
        return 100*(piece_count - opp_piece_count)/(piece_count + opp_piece_count)
        
    
    def evaluate_mobility(self, board):
        mobility = len(board.get_potential_moves(self.player))
        opp_mobility = len(board.get_potential_moves((self.player%2)+1))
        
        if (mobility + opp_mobility) == 0:
            return 0
        
        return 100*(mobility - opp_mobility)/(mobility + opp_mobility)
        
        
    def evaluate_corners(self, board):
        corner_count = board.board[0][0]==self.player + \
                        board.board[0][7]==self.player + \
                        board.board[7][0]==self.player + \
                        board.board[7][7]==self.player
        opp_corner_count = board.board[0][0]==((self.player%2)+1) + \
                        board.board[0][7]==((self.player%2)+1) + \
                        board.board[7][0]==((self.player%2)+1) + \
                        board.board[7][7]==((self.player%2)+1)
                        
        if (corner_count + opp_corner_count) == 0:
            return 0
        
        return 100*(corner_count - opp_corner_count)/(corner_count + opp_corner_count)
        
        
    def evaluate_static_weights(self, board):
        static_weights = [[4,  -3,  2,  2,  2,  2, -3,  4],
                          [-3, -4, -1, -1, -1, -1, -4, -3],
                          [2,  -1,  1,  0,  0,  1, -1,  2],
                          [2,  -1,  0,  1,  1,  0, -1,  2],
                          [2,  -1,  0,  1,  1,  0, -1,  2],
                          [2,  -1,  1,  0,  0,  1, -1,  2],
                          [-3, -4, -1, -1, -1, -1, -4, -3],
                          [4,  -3,  2,  2,  2,  2, -3,  4]]
        
        piece_locations = [[static_weights[x][y] if board.board[x][y] == self.player else 0 
                            for y in range(len(board.board)) ] 
                           for x in range(len(board.board))]
        opp_piece_locations = [[static_weights[x][y] if board.board[x][y] == (self.player%2)+1 else 0 
                            for y in range(len(board.board)) ] 
                           for x in range(len(board.board))]
        
        total_weight = sum(map(sum, piece_locations))
        opp_total_weight = sum(map(sum, opp_piece_locations))
        
        return total_weight-opp_total_weight
        
        
    def evaluate(self, board):
        score = 0
        
        piece_count = self.evaluate_piece_count(board)
        mobility = self.evaluate_mobility(board)
        corners = self.evaluate_corners(board)
        static_weights = self.evaluate_static_weights(board)
        
        score += 0.5*piece_count
        score += 2*mobility
        score += 5*corners
        score += 5*static_weights
        
        return score
        
        
    def minimax(self, board, player, depth=2, alpha=-math.inf, beta=math.inf):
        moves = board.get_actual_moves(player)
        # Move ordering here
        
        if not moves:
            return None, self.evaluate(board)
        
        if depth == 0: 
            return None, self.evaluate(board)
        
        if player == self.player:
            best_move = None
            best_val = -math.inf
            for move in moves:
                # print('self')
                last_state = board.move(move, player)
                # print(board)
                _, val = self.minimax(board, (player%2)+1, depth-1, alpha, beta)
                board.undo_move(last_state)
                if val > best_val:
                    best_move = move
                    best_val = val
                alpha = max(alpha, val)
                if alpha >= beta:
                    break
            return best_move, best_val
        
        else:
            best_val = math.inf
            for move in moves:
                # print('other')
                last_state = board.move(move, player)
                # print(board)
                _, val = self.minimax(board, (player%2)+1, depth, alpha, beta)
                board.undo_move(last_state)
                best_val = min(best_val, val)
                beta = min(beta, val)
                if alpha >= beta:
                    break
            return None, best_val
        