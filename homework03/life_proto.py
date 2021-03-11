import pygame
import random

from pygame.locals import *
from typing import List, Tuple


Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:
    def __init__(
        self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10
    ) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))
        self.grid = self.create_grid(True)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:  # type: ignore
                    running = False
            self.draw_lines()
            self.grid = self.get_next_generation()
            self.draw_grid()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        if randomize:
            return [
                [random.randint(0, 1) for _ in range(self.cell_width)]
                for _ in range(self.cell_height)
            ]
        return [[0 for _ in range(self.cell_width)] for _ in range(self.cell_height)]

    def draw_grid(self) -> None:
        for pos_x, row in enumerate(self.grid):
            for pos_y, col in enumerate(row):
                color = pygame.Color("white")
                if col:
                    color = pygame.Color("green")
                pygame.draw.rect(
                    self.screen,
                    color,
                    (
                        self.cell_size * pos_y + 1,
                        self.cell_size * pos_x + 1,
                        self.cell_size - 1,
                        self.cell_size - 1,
                    ),
                )

    def get_neighbours(self, cell: Cell) -> Cells:
        neighbours = []
        rows = len(self.grid)
        cols = len(self.grid[0]) if rows else 0
        for i in range(max(0, cell[0] - 1), min(rows, cell[0] + 2)):
            for j in range(max(0, cell[1] - 1), min(cols, cell[1] + 2)):
                if (i, j) != cell:
                    neighbours.append(self.grid[i][j])
        return neighbours

    def get_next_generation(self) -> Grid:
        new_grid = self.create_grid()
        for pos_x, row in enumerate(self.grid):
            for pos_y, col in enumerate(row):
                pos = (pos_x, pos_y)
                neigh = sum(self.get_neighbours(pos))
                if col:
                    if neigh != 2 and neigh != 3:
                        new_grid[pos_x][pos_y] = 0
                    else:
                        new_grid[pos_x][pos_y] = 1
                else:
                    if neigh == 3:
                        new_grid[pos_x][pos_y] = 1
        return new_grid


if __name__ == "__main__":
    game = GameOfLife(320, 240, 20)
    game.run()
