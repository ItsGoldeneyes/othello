
class Minimax:
    def __init__(self):
        pass
    
    def move(self, board):
        self.board = board
        
        move, val = self.minimax(board)
        return move
    
    def minimax(self, )