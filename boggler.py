BOARD_SIZE = 3
MIN_WORD_LENGTH = 3

test_board = [('a', 'b', 'c'),
              ('d', 'e', 'f'),
              ('g', 'h', 'i')]

test_board2 = [('b', 'a', 'r'),
              ('e', 'c', 'n'),
              ('l', 'a', 'o')]


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

def get_neighbours(v):
    row = v[0]
    column = v[1]
    return [(r, c) for r in [row - 1, row, row + 1] for c in [column - 1, column, column + 1]
            if (not (r == row and c == column)) and (1 <= r <= BOARD_SIZE and 1 <= c <= BOARD_SIZE)]

assert get_neighbours((2, 2)) == [(1, 1), (1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2), (3, 3)]
assert get_neighbours((1, 1)) == [(1, 2), (2, 1), (2, 2)]


def dfs(graph, vertex):
    """
    graph - a square list of tuples,
    vertex - a Node representing the starting cell
    """
    results = []

    def visit(node, visited, word_so_far):
        visited.append(node)
        word_so_far += graph[node[0] - 1][node[1] - 1]
        if len(word_so_far) >= MIN_WORD_LENGTH:
            results.append(word_so_far)
        neighbours = get_neighbours(node)
        for next_coordinates in neighbours:
            next_node = (next_coordinates[0], next_coordinates[1])
            if not next_node in visited:
                visit(next_node, list(visited), word_so_far)

    visit(vertex, [vertex], "")
    return results


class BoggleSolver:
    def __init__(self, list_of_lists):
        assert len(list_of_lists) == BOARD_SIZE
        assert all(len(row) == BOARD_SIZE for row in list_of_lists)
        self.set_game_board(list_of_lists)

    def set_game_board(self, list_of_lists):
        self.board = list_of_lists

    def print_board(self):
        for row in self.board:
            print(row)

    def play(self):
        return []

# Now let's play some Boggle!

result = []
for start in [(r, c) for r in range(1, BOARD_SIZE + 1) for c in range(1, BOARD_SIZE + 1)]:
    words_at_start = dfs(test_board2, start)
    print("found %d paths starting at %s" %(len(words_at_start), start,))
    result = result + words_at_start

for line in result:
    if line in dictionary_list:
        print("found a word! : %s" % line)


# OK that works, but it is slow as hell, because we keep looking for all possible paths, even when it's obviously not
# leading to any real word! We need to add pruning of hopeless paths, and we can do it if we convert our dictionary into
# a TRIE.

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
