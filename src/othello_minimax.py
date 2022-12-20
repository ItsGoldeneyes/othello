import math


class Minimax:
    
    def __init__(self):
        pass
    
    
    def move(self, board, player):
        self.board = board
        self.player = player
        
        best_move = [(0, 0), -(math.inf)]
        for move in board.get_possible_moves(player):
            _, val = self.minimax(board, player)
            
            if val > best_move[1]:
                best_move = [move, val]
        return best_move[0]
    
    
    def evaluate(self, board, player):
        if player == 1:
            return board.count_pieces(1) - board.count_pieces(2)
        else:
            return board.count_pieces(2) - board.count_pieces(1)
    
    
    def minimax(self, board, player, depth=3, alpha=-math.inf, beta=math.inf):
        moves = board.get_possible_moves(player)
        if not moves:
            return None, self.evaluate(board, player)
        
        if depth == 0: 
            return None, self.evaluate(board, player)
        
        if player == self.player:
            print('self')
            best_move = None
            best_val = -math.inf
            for move in moves:
                board.move(move, player)
                _, val = self.minimax(board, (player%2)+1, depth-1, alpha, beta)
                board.undo_move()
                if val > best_val:
                    best_move = move
                    best_val = val
                alpha = max(alpha, val)
                if alpha >= beta:
                    break
            return best_move, best_val
        
        else:
            print('other')
            best_val = math.inf
            for move in moves:
                board.move(move, player)
                _, val = self.minimax(board, (player%2)+1, depth-1, alpha, beta)
                board.undo_move()
                best_val = min(best_val, val)
                beta = min(beta, val)
                if alpha >= beta:
                    break
            return None, best_val
        