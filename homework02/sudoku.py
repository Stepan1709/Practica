import pathlib
import typing as tp

T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    """ Прочитать Судоку из указанного файла """
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: tp.List[tp.List[str]]) -> None:
    """Вывод Судоку """
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print(
            "".join(
                grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9)
            )
        )
        if str(row) in "25":
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    c = []
    m = []
    b = 0
    for i in values:
        b += 1
        m += [i]
        if b % n == 0 or b == len(values):
            c += [m]
            m = []
    return c

def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    return grid[pos[0]]

def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    c = []
    for i in grid:
        c += [i[pos[1]]]
    return c


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    if pos[0] < 3:
        a = 0
    elif 3 <= pos[0] < 6:
        a = 3
    else:
        a = 6
    if pos[1] < 3:
        b = 0
    elif 3 <= pos[1] < 6:
        b = 3
    else:
        b = 6
    return grid[a][b:b + 3] + grid[a + 1][b:b + 3] + grid[a + 2][b:b + 3]


def find_empty_positions(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.Tuple[int, int]]:
    a = -1
    for i in range(len(grid)):
        if '.' in grid[i]:
            a = i
            break
    for i in range(len(grid[a])):
        if grid[a][i] == '.':
            b = i
            break
    if a == -1:
        return(False)
    else:
        return (a, b)



def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    v = {'1', '2', '3', '4', '5', '6', '7', '8', '9'}
    a = set(get_row(grid, pos))
    a.update(set(get_col(grid, pos)))
    a.update(set(get_block(grid, pos)))
    return (v - a)


def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    d = find_empty_positions(grid)
    if d:
        v = find_possible_values(grid, d)
        if len(v) != 0:
            for i in v:
                grid[d[0]][d[1]] = i
                a = solve(grid)
                if a:
                    return a
                else:
                    grid[d[0]][d[1]] = '.'

        else:
            return False
    else:
        return grid



def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    if find_empty_positions(solution):
        return False
    for i in range(9):
        a = get_row(solution, (i, 0))
        b = get_col(solution, (0, i))
        c = get_block(solution, ((i // 3 * 3), (i % 3 * 3)))
        if len(a) == len(set(a)) and len(b) == len(set(b)) and len(c) == len(set(c)):
            ...
        else:
            return False
    return True

import random

def generate_sudoku(N: int) -> tp.List[tp.List[str]]:
    c = [['1', '2', '3', '4', '5', '6', '7', '8', '9'],
         ['4', '5', '6', '7', '8', '9', '1', '2', '3'],
         ['7', '8', '9', '1', '2', '3', '4', '5', '6'],
         ['2', '3', '4', '5', '6', '7', '8', '9', '1'],
         ['5', '6', '7', '8', '9', '1', '2', '3', '4'],
         ['8', '9', '1', '2', '3', '4', '5', '6', '7'],
         ['3', '4', '5', '6', '7', '8', '9', '1', '2'],
         ['6', '7', '8', '9', '1', '2', '3', '4', '5'],
         ['9', '1', '2', '3', '4', '5', '6', '7', '8']]
    if N >= 81:
        N = 81
    b = 81 - N
    while b > 0:
        x = random.randint(0, 8)
        y = random.randint(0, 8)
        if c[y][x] != '.':
            c[y][x] = '.'
            b -= 1
    return c


if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)
