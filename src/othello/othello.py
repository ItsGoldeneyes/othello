from othello.othello_board import OthelloBoard
import re

class OthelloGame():
    '''
    Othello game class
    Creates a game of Othello based on the OthelloBoard class
    Iterate through turns using turn function
    '''
    def __init__(self, debug=False):
        self.board = OthelloBoard(debug=debug)
        self.winner = False
        self.stalemate_timer = 0
        self.debug = debug

    def show(self):
        print(self.board)

    def reset(self):
        self.board = OthelloBoard(debug=self.debug)
        self.winner = False
        self.stalemate_timer = 0
    
    def extract_pos(self, pos_str):
        '''
        Get position from input using regex
        Converts input to tuple of (row, col) indexed from 0
        From user input assumed to be indexed from 1
        '''
        first = re.search(r"\d", pos_str)
        if first == None:
            raise ValueError("Input contains no numbers")
        
        second = re.search(r"\d+", pos_str[first.start()+1:])
        if second == None:
            raise ValueError("Input contains only one number")
        
        return (int(second.group())-1, int(first.group())-1)
            
    def turn(self, player, pos= False):
        '''
        Takes a turn for a given player
        If pos is given, it will attempt to move there, otherwise it will ask for user input
        '''
        assert player == 1 or player == 2
        
        # Check for stalemate
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
            if not self.board.check_move(pos, player):
                return False
            else:
                self.board.move(pos, player)
                
        else:
            valid = False
            # While the move is invalid, ask for input
            while not valid:
                pos_input = input(f"Where would player {player} like to move?")
                pos_tuple = False
                
                try: 
                    pos_tuple = self.extract_pos(pos_input)
                except ValueError as e:
                    print(e)
                if pos_tuple:
                    valid = self.board.check_move(pos_tuple, player)
                if not valid:
                    print("Invalid move!")
                    
            self.board.move(pos_tuple, player)
        
        # Check for winner
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