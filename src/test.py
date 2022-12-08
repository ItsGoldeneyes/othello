import unittest

from othello import OthelloBoard, OthelloGame


class BoardDefaultTest(unittest.TestCase):
    def setUp(self):
        self.board = OthelloBoard()
        
    def test_board_default_height(self):
        # Arrange
        expected_size = 8

        # Act
        result_size = len(self.board.board[0])

        # Assert
        self.assertEqual(expected_size, result_size)
        self.assertEqual(expected_size, len(self.board.board[0]))
        
    def test_board_default_width(self):
        # Arrange
        expected_size = 8

        # Act
        result_size = len(self.board.board)

        # Assert
        self.assertEqual(expected_size, result_size)
        self.assertEqual(expected_size, len(self.board.board[0]))
        
    def test_board_default_positions(self):

        # Assert
        self.assertEqual(self.board.board[4][4], 1)
        self.assertEqual(self.board.board[3][3], 1)
        self.assertEqual(self.board.board[4][3], 2)
        self.assertEqual(self.board.board[3][4], 2)
        
class BoardAdjacentTest(unittest.TestCase):
    def setUp(self):
        self.board = OthelloBoard()
        
    def test_adjacent_center(self):
        # Arrange
        test_pos = (4, 4)
        expected_adjacent = {"n": (4, 5), "ne": (5, 5), "e": (5, 4), "se": (5, 3), "s": (4, 3), "sw": (3, 3), "w": (3, 4), "nw": (3, 5)}

        # Act
        result_adjacent = self.board.adjacent_spaces(test_pos, True)

        # Assert
        self.assertEqual(expected_adjacent, result_adjacent)
    
    def test_adjacent_top_left(self):
        # Arrange
        test_pos = (0, 7)
        expected_adjacent = {"s": (0, 6), "se": (1, 6), "e": (1, 7)}

        # Act
        result_adjacent = self.board.adjacent_spaces(test_pos, True)

        # Assert
        self.assertEqual(expected_adjacent, result_adjacent)
        
    def test_adjacent_top_right(self):
        # Arrange
        test_pos = (7, 7)
        expected_adjacent = {"s": (7, 6), "sw": (6, 6), "w": (6, 7)}

        # Act
        result_adjacent = self.board.adjacent_spaces(test_pos, True)

        # Assert
        self.assertEqual(expected_adjacent, result_adjacent)
        
    def test_adjacent_bottom_left(self):
        # Arrange
        test_pos = (0, 0)
        expected_adjacent = {"n": (0, 1), "ne": (1, 1), "e": (1, 0)}

        # Act
        result_adjacent = self.board.adjacent_spaces(test_pos, True)

        # Assert
        self.assertEqual(expected_adjacent, result_adjacent)
        
    def test_adjacent_bottom_right(self):
        # Arrange
        test_pos = (7, 0)
        expected_adjacent = {"n": (7, 1), "nw": (6, 1), "w": (6, 0)}

        # Act
        result_adjacent = self.board.adjacent_spaces(test_pos, True)

        # Assert
        self.assertEqual(expected_adjacent, result_adjacent)

class BoardFloodfillTest(unittest.TestCase):
    def setUp(self):
        self.board = OthelloBoard()
    
    def test_floodfill_player_1_west(self):
        # Arrange
        orig_pos = (5, 3)
        direction = 'w'
        test_pos = self.board.adjacent_spaces(orig_pos, directional=True)[direction]
        expected_floodfill = [(4,3)]

        # Act
        result_floodfill = self.board.floodfill(test_pos, 1, direction)

        # Assert
        self.assertEqual(expected_floodfill, result_floodfill)
    
    def test_floodfill_player_1_east(self):
        # Arrange
        orig_pos = (2, 4)
        direction = 'e'
        test_pos = self.board.adjacent_spaces(orig_pos, directional=True)[direction]
        expected_floodfill = [(3,4)]

        # Act
        result_floodfill = self.board.floodfill(test_pos, 1, direction)

        # Assert
        self.assertEqual(expected_floodfill, result_floodfill)
    
    def test_floodfill_player_1_south(self):
        # Arrange
        orig_pos = (3, 5)
        direction = 's'
        test_pos = self.board.adjacent_spaces(orig_pos, directional=True)[direction]
        expected_floodfill = [(3,4)]

        # Act
        result_floodfill = self.board.floodfill(test_pos, 1, direction)

        # Assert
        self.assertEqual(expected_floodfill, result_floodfill)
    
    def test_floodfill_player_1_north(self):
        # Arrange
        orig_pos = (4, 2)
        direction = 'n'
        test_pos = self.board.adjacent_spaces(orig_pos, directional=True)[direction]
        expected_floodfill = [(4,3)]

        # Act
        result_floodfill = self.board.floodfill(test_pos, 1, direction)

        # Assert
        self.assertEqual(expected_floodfill, result_floodfill)
        
    def test_floodfill_player_2_west(self):
        # Arrange
        orig_pos = (5, 4)
        direction = 'w'
        test_pos = self.board.adjacent_spaces(orig_pos, directional=True)[direction]
        expected_floodfill = [(4,4)]

        # Act
        result_floodfill = self.board.floodfill(test_pos, 2, direction)

        # Assert
        self.assertEqual(expected_floodfill, result_floodfill)
        
    def test_floodfill_player_2_east(self):
        # Arrange
        orig_pos = (2, 3)
        direction = 'e'
        test_pos = self.board.adjacent_spaces(orig_pos, directional=True)[direction]
        expected_floodfill = [(3,3)]

        # Act
        result_floodfill = self.board.floodfill(test_pos, 2, direction)

        # Assert
        self.assertEqual(expected_floodfill, result_floodfill)
        
    def test_floodfill_player_2_south(self):
        # Arrange
        orig_pos = (4, 5)
        direction = 's'
        test_pos = self.board.adjacent_spaces(orig_pos, directional=True)[direction]
        expected_floodfill = [(4,4)]

        # Act
        result_floodfill = self.board.floodfill(test_pos, 2, direction)

        # Assert
        self.assertEqual(expected_floodfill, result_floodfill)
        
    def test_floodfill_player_2_north(self):
        # Arrange
        orig_pos = (3, 2)
        direction = 'n'
        test_pos = self.board.adjacent_spaces(orig_pos, directional=True)[direction]
        expected_floodfill = [(3,3)]

        # Act
        result_floodfill = self.board.floodfill(test_pos, 2, direction)

        # Assert
        self.assertEqual(expected_floodfill, result_floodfill)
        
    def test_floodfill_player_1_self(self):
        # Arrange
        orig_pos = (3, 2)
        direction = 'n'
        test_pos = self.board.adjacent_spaces(orig_pos, directional=True)[direction]
        expected_floodfill = False

        # Act
        result_floodfill = self.board.floodfill(test_pos, 1, direction)

        # Assert
        self.assertEqual(expected_floodfill, result_floodfill)
    
    def test_floodfill_player_2_self(self):
        # Arrange
        orig_pos = (3, 3)
        direction = 'n'
        test_pos = self.board.adjacent_spaces(orig_pos, directional=True)[direction]
        expected_floodfill = False

        # Act
        result_floodfill = self.board.floodfill(test_pos, 1, direction)

        # Assert
        self.assertEqual(expected_floodfill, result_floodfill)
        
        
    def test_floodfill_player_1_complex(self):
        # Arrange
        self.board.move(1, (4,2))
        self.board.move(2, (5,2))
        
        orig_pos = (3, 5)
        direction = 's'
        test_pos = self.board.adjacent_spaces(orig_pos, directional=True)[direction]
        expected_floodfill = [(3,4)]

        # Act
        result_floodfill = self.board.floodfill(test_pos, 1, direction)

        # Assert
        self.assertEqual(expected_floodfill, result_floodfill)
        
        
def run_tests():
    # Run only the tests in the specified classes

    test_classes_to_run = [BoardFloodfillTest] # [BoardDefaultTest, BoardAdjacentTest, BoardFloodfillTest]

    loader = unittest.TestLoader()

    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)
        
    big_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)

if __name__ == "__main__":
    run_tests()

# if __name__ == '__main__':
#     unittest.main()