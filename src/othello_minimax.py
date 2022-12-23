import math


class Minimax:
    
    def __init__(self):
        pass
    
    
    def move(self, board, player):
        self.board = board
        self.player = player
        
        best_move = [(0, 0), -(math.inf)]
        for move in board.get_possible_moves(player):
            _, val = self.minimax(board, player, depth=3)
            
            if val > best_move[1]:
                best_move = [move, val]
        return best_move[0]
    
    
    def evaluate(self, board):
        score = 0
        piece_count = board.count_pieces(self.player)
        opp_piece_count = board.count_pieces((self.player%2)+1)
        
        corner_count = board.board[0][0]==self.player + \
                        board.board[0][7]==self.player + \
                        board.board[7][0]==self.player + \
                        board.board[7][7]==self.player       
        opp_corner_count = board.board[0][0]==((self.player%2)+1) + \
                        board.board[0][7]==((self.player%2)+1) + \
                        board.board[7][0]==((self.player%2)+1) + \
                        board.board[7][7]==((self.player%2)+1)
        
        edges = [x[0] for x in board.board] + \
                [x[7] for x in board.board] + \
                board.board[0][1:6] + board.board[7][1:6]
        edge_count = edges.count(self.player)
        opp_edge_count = edges.count((self.player%2)+1)
        
        # safe_pieces = board.get_safe_pieces(self.player)
        
        
        score += corner_count*5
        score -= opp_corner_count*2
        score += edge_count//2
        score -= opp_edge_count//4
        score += piece_count
        
        return score
        
        
    def minimax(self, board, player, depth=2, alpha=-math.inf, beta=math.inf):
        moves = board.get_possible_moves(player)
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
        