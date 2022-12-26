from othello.othello import OthelloGame
import othello_minimax as om
import time

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
        return self.game.winner

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
                print('Minimax is thinking...')
                move = mm.move(self.game.board, player)
                self.game.turn(2, pos=move)
                self.game.show()
                
            player = (player%2)+1
        return self.game.winner
    
    def play_minimax_v_minimax(self):
        self.game.reset()
        player = 1
        self.game.show()
        mm = om.Minimax()
        
        while not self.game.winner:
            print('Minimax is thinking...')
            move = mm.move(self.game.board, player)
            self.game.turn(player, pos=move)
            self.game.show()
                
            player = (player%2)+1
        return self.game.winner

if __name__ == "__main__":
    game = Othello()
    
    winner = game.play_minimax()
    
    print(f"Player {winner} wins!")
    print(f' P1: {game.game.board.count_pieces(1)} - P2: {game.game.board.count_pieces(2)}')