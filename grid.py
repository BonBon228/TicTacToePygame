import pygame
from cell import Cell


# Class representing the game grid
class Grid:
    # Initialize the grid with a renderer, dimensions, cell size, and margin
    def __init__(self, renderer, width, height, cell_size, margin):
        self.renderer = renderer
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.margin = margin
        self.cells = []
        self.initialize_grid()

    # Initialize the grid by creating individual cells
    def initialize_grid(self):
        for i in range(self.margin, self.width - self.margin, self.cell_size):
            for j in range(self.margin, self.height - self.margin, self.cell_size):
                self.cells.append(Cell(i, j, self.renderer))

    # Draw the grid lines on the screen
    def draw_grid(self):
        line_color = (70, 130, 180)
        for i in range(self.margin, self.width, self.cell_size):
            self.renderer.draw_line((i, self.margin), (i, self.height - self.margin), line_color)
        for j in range(self.margin, self.height, self.cell_size):
            self.renderer.draw_line((self.margin, j), (self.width - self.margin, j), line_color)

    # Check if all cells in the grid are filled
    def is_cells_filled(self):
        for cell in self.cells:
            if cell.filled_player is None:
                return False
        return True

    # Handle a click on a cell in the grid
    def click_cell(self, position, player):
        x, y = position
        for cell in self.cells:
            if cell.filled_player is None:
                if cell.x < x < cell.x + self.cell_size and cell.y < y < cell.y + self.cell_size:
                    if cell.is_adjacent_filled(self.cells, self.cell_size) or all(c.filled_player is None for c in self.cells):
                        cell.fill_cell(player, self.cell_size)
                        return True
        return False
    
    # Check if the current player has won the game
    def check_win(self, player):
        for cell in self.cells:
            if cell.filled_player == player:
                # Check horizontal, vertical, and diagonal lines
                for dx, dy in [(1, 0), (0, 1), (1, 1), (1, -1)]:
                    winning_cells = [cell]
                    for dist in range(1, 5):
                        x, y = cell.x + dist * dx * self.cell_size, cell.y + dist * dy * self.cell_size
                        for c in self.cells:
                            if c.x == x and c.y == y and c.filled_player == player:
                                winning_cells.append(c)
                                break
                        else:
                            break
                    else:
                        return winning_cells
        return []

    # Highlight the cells that form a winning combination
    def highlight_cells(self, cells):
        if cells:
            dx = cells[-1].x - cells[0].x
            dy = cells[-1].y - cells[0].y
            if abs(dx) == abs(dy):  # diagonal movement
                if dx == dy:  # decreasing diagonal
                    start = (cells[0].x, cells[0].y)
                    end = (cells[-1].x + self.cell_size, cells[-1].y + self.cell_size)
                else:  # increasing diagonal
                    start = (cells[0].x, cells[0].y + self.cell_size)
                    end = (cells[-1].x + self.cell_size, cells[-1].y)
            elif dx != 0:  # horizontal movement
                start = (cells[0].x, cells[0].y + self.cell_size // 2)
                end = (cells[-1].x + self.cell_size, cells[-1].y + self.cell_size // 2)
            else:  # vertical movement
                start = (cells[0].x + self.cell_size // 2, cells[0].y)
                end = (cells[-1].x + self.cell_size // 2, cells[-1].y + self.cell_size)
            pygame.draw.line(self.renderer.screen, (0, 0, 0), start, end, self.cell_size // 10)