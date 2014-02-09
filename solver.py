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
Match = namedtuple('Match', 'index, block, length')
Move = namedtuple('Move', 'row, column, block, offset, match_length')



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
    from itertools import groupby
    groups = [Match(0, k, len(list(g))) for k, g in groupby(row)]
    # 0 above is placeholder for index, update it to real value
    for i, cur in list(enumerate(groups))[1:]:
        prev = groups[i - 1]
        groups[i] = cur._replace(index=prev.index + prev.length)
    return [g for g in groups if g.length >= min_length]


def find_matches(grid):
    fmir = find_matches_in_row
    hor = [(i, fmir(r)) for i, r in enumerate(grid) if fmir(r)]
    ver = [(i, fmir(r)) for i, r in enumerate(transpose(grid)) if fmir(r)]
    return hor, ver


def clear_on_axis(grid, axis_matches):
    for i, matches in axis_matches.items():
        row = grid[i]
        for m in matches:
            row[m.index:m.index + m.length] = 'U' * m.length


def clear_matches(grid):
    grid = [list(g) for g in grid]  # make a deep copy
    hor, ver = [dict(m) for m in find_matches(grid)]

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

#print_grid(clear_matches(grid))
#print_grid(collapse_matches(clear_matches(grid)))

print find_moves_on_axis(grid)
