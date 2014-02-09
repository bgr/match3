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
        print ''.join([str(i + 1) + ' '] + s)


grid = get_random_grid()
print_grid(grid)


def column(grid, col_num):
    return [row[col_num] for row in grid]


def transpose(grid):
    return [column(grid, i) for i in range(len(grid))]
