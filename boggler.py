__author__ = 'akarpov'


test_board = [('a', 'b', 'c', 'd'),
              ('a', 'b', 'c', 'd'),
              ('a', 'b', 'c', 'd'),
              ('a', 'b', 'c', 'd')]


class BoggleSolver:

    def __init__(self, list_of_lists):
        assert len(list_of_lists) == 4
        assert all(len(row) == 4 for row in list_of_lists)
        self.set_game_board(list_of_lists)

    def set_game_board(self, list_of_lists):
        self.board = list_of_lists

    def print_board(self):
        for row in self.board:
            print(row)

    def build_trie(self, x, y):



game = BoggleSolver(test_board)
game.print_board()
