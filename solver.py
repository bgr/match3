colors = [
    'B',  # backpack
    'A',  # armor
    'W',  # wood
    'R',  # rock
    'K',  # key
    'M',  # magic
    'S',  # sword
    'J',  # joker
]

terminal_colors = {
    'B': 212,
    'A': 23,
    'W': 52,
    'R': 243,
    'K': 112,
    'M': 160,
    'S': 19,
    'J': 51,
    'U': 232,  # unknown empty tile that remains after matching
}


from collections import namedtuple
Match = namedtuple('Match', 'index, tile, length')
Move = namedtuple('Move', 'row, column, tile, offset, match_length')



def get_random_grid(size=8):
    import random
    return [[random.choice(colors) for _ in range(size)] for _ in range(size)]


def colorize(text, color):
    return '\x1b[48;5;%(color)sm%(text)s\x1b[0m' % locals()


def print_grid(grid):
    print '   A B C D E F G H'
    for i, row in enumerate(grid):
        s = [colorize(elem + ' ', terminal_colors[elem]) for elem in row]
        print ''.join([str(i) + ' '] + s)


def column(grid, col_num):
    return [row[col_num] for row in grid]


def transpose(grid):
    return [column(grid, i) for i in range(len(grid))]


def find_matches_in_row(row, min_length=3):
    def grouper(acc_matches, next_tile):
        if not acc_matches:  # got first element in the row
            return [Match(0, next_tile, 1)]
        ms, m = acc_matches[:-1], acc_matches[-1]
        if m.tile == next_tile:
            return ms + [m._replace(length=m.length + 1)]
        else:
            return acc_matches + [Match(m.index + m.length, next_tile, 1)]

    # create matches, consecutive blocks will be grouped together
    foo = Match(0, 'U', 0)  # makes it easier not having to check list index
    matches = [foo] + reduce(grouper, row, []) + [foo]

    i = 1
    while i < len(matches) - 1:
        prev, cur, nxt = matches[i - 1], matches[i], matches[i + 1]
        if cur.tile == 'J':
            if prev.tile == nxt.tile:  # joker between same tiles, join all
                matches[i - 1] = prev._replace(
                    length=prev.length + cur.length + nxt.length)
                matches.remove(cur)
                matches.remove(nxt)
            else:  # joker between different tiles, enlarge both & remove joker
                matches[i - 1] = prev._replace(
                    length=prev.length + cur.length)
                matches[i + 1] = nxt._replace(
                    index=cur.index,
                    length=cur.length + nxt.length)
                matches.remove(cur)
        else:
            i += 1
    return [m for m in matches if m.length >= min_length and m.tile != 'U']


# too lazy to do proper testing
tests = [
    ('ABA', []),
    ('AAA', [Match(0, 'A', 3)]),
    ('XAAABBBBCCCCC', [Match(1, 'A', 3), Match(4, 'B', 4), Match(8, 'C', 5)]),
    ('JJJ', []),  # jokers aren't counted by themselves
    ('JBBAJADDJ', [Match(0, 'B', 3), Match(3, 'A', 3), Match(6, 'D', 3)]),
    ('AAJBB', [Match(0, 'A', 3), Match(2, 'B', 3)]),
    ('BBBAJAJACCC', [Match(0, 'B', 3), Match(3, 'A', 5), Match(8, 'C', 3)]),
]  # TODO: test with U tiles
for arg, expected in tests:
    res = find_matches_in_row(arg, min_length=3)
    assert res == expected, (arg, res, expected)


def find_matches(grid):
    fmir = find_matches_in_row
    hor = [(i, fmir(r)) for i, r in enumerate(grid) if fmir(r)]
    ver = [(i, fmir(r)) for i, r in enumerate(transpose(grid)) if fmir(r)]
    return hor, ver


def clear_matches(grid):
    grid = [list(g) for g in grid]  # make a deep copy
    hor, ver = [dict(m) for m in find_matches(grid)]

    def clear_on_axis(grid, axis_matches):
        for i, matches in axis_matches.items():
            row = grid[i]
            for m in matches:
                row[m.index:m.index + m.length] = 'U' * m.length

    clear_on_axis(grid, hor)
    grid = transpose(grid)
    clear_on_axis(grid, ver)
    return transpose(grid)


def collapse_matches(cleared_grid):
    cols = [list(''.join(col).replace('U', '').rjust(len(cleared_grid), 'U'))
            for col in transpose(cleared_grid)]
    return transpose(cols)


def moves_for_row(grid, row_index):
    row = grid[row_index]
    for i_col, _ in enumerate(row):
        col = column(grid, i_col)
        for col_shift, col_elem in enumerate(col):
            row_test = list(row)
            row_test[i_col] = col_elem
            row_matches = find_matches_in_row(row_test)
            for m in row_matches:
                offset = row_index - col_shift
                move = Move(row_index, i_col, col_elem, offset, m.length)
                yield move


def find_moves_on_axis(grid):
    """ Returns all possible moves that will result in horizontal matches."""
    moves = {}
    for i, _ in enumerate(grid):
        row_moves = list(moves_for_row(grid, i))
        if row_moves:
            moves[i] = row_moves
    return moves


grid = get_random_grid()
print_grid(grid)

print_grid(clear_matches(grid))

tmp_grid = grid
while True:
    collapsed = collapse_matches(clear_matches(tmp_grid))
    print_grid(collapsed)

    tmp_grid = clear_matches(collapsed)
    if tmp_grid == collapsed:
        break
    else:
        print '\nCASCADE!\n'
        print_grid(tmp_grid)
