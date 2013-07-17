test_board = [('a', 'b', 'c', 'd'),
              ('a', 'b', 'c', 'd'),
              ('a', 'b', 'c', 'd'),
              ('a', 'b', 'c', 'd')]


def is_acceptable(word):
    """
    Check whether a word is acceptable for Boggle. House rules: no names!
    """
    def is_lowercase(w):
        return 97 <= ord(w[0]) <= 122

    def is_possessive(w):
        return word.strip()[-2:] == "'s"

    return is_lowercase(word) and (not is_possessive(word))

# Um... let's call this a testing suite.
assert is_acceptable("marketplace") and not is_acceptable("zygote's") and not is_acceptable("Albert")


def filter_acceptable(list_of_words):
    return [word.strip() for word in list_of_words if is_acceptable(word)]

# borrow Unix built-in dictionary
dictionary_list = filter_acceptable([line for line in open('/usr/share/dict/words', 'r')])
print("built a dictionary of %d English words" % (len(dictionary_list)))
# ..and turn it into a trie.


def build_trie(words):
    """
    Create a trie out of a flat list of words. Trie will be a dict of dicts (of dicts, etc).
    Example:
    ["foo","foobar","bar","baz"] =>
    {f:
     {o:
      {o: { None: None},
       b:
        {a:
         {r: {None: None }}}}},
     b:
      {a:
       {r: {None: None},
        z:{None: None}}}}
    """
    # we'll have 26 choices on the first level
    root_dict = {}
    for word in words:
        current_dict = root_dict
        # start adding letters to the dict on the corresponding level, beginning with root
        for letter in word:
            current_dict = current_dict.setdefault(letter, {})
        # a word is now represented with keys in nested dicts -- terminate it with None
        current_dict = current_dict.setdefault(None, None)
    return root_dict


class Node:
    def __init__(self, row, column, letter):
        assert 1 <= row <= 4 and 1 <= column <= 4
        self.row = row
        self.column = column
        # self.up = (row - 1 if row > 1 else None)
        # self.down = (row + 1 if row < 3 else None)
        # self.left = (column - 1 if column > 1 else None)
        # self.right = (column + 1 if column < 3 else None)
        self.letter = letter


def get_neighbours(row, column):
    return [(r, c) for r in [row - 1, row, row + 1] for c in [column - 1, column, column + 1]
            if (not (r == row and c == column)) and not (r == 0 or c == 0)]

assert get_neighbours(2, 2) == [(1, 1), (1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2), (3, 3)]
assert get_neighbours(1, 1) == [(1, 2), (2, 1), (2, 2)]


def dfs(graph, vertex):
    """
    graph - a square list of tuples,
    vertex - a Node representing the starting cell
    """


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

    def play(self):
        return []


game = BoggleSolver(test_board)
game.print_board()
