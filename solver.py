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
    'U': 232,
}


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


from collections import namedtuple
Match = namedtuple('Match', 'index, block, length')


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


grid = get_random_grid()
print_grid(grid)

print_grid(clear_matches(grid))
