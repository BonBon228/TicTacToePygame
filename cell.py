import pygame


# Class representing an individual cell in the grid
class Cell:
    # Initialize a cell with a position and ui
    def __init__(self, x, y, ui):
        self.x = x
        self.y = y
        self.ui = ui
        self.filled_player = None

    # Fill the cell with a player's symbol
    def fill_cell(self, player, cell_size):
        if self.filled_player is None:
            self.filled_player = player
            self.draw(cell_size)
            print(f'Cell filled at {self.x}, {self.y} by player {self.filled_player}')

    # Draw the filled cell on the screen
    def draw(self, cell_size):
        if self.filled_player is not None:
            image = pygame.transform.scale(self.filled_player.image_symbol, (cell_size, cell_size))
            self.ui.screen.blit(image, (self.x, self.y))

    # Check if any adjacent cells are already filled
    def is_adjacent_filled(self, cells, cell_size):
        for cell in cells:
            if cell.filled_player is not None:
                if abs(cell.x - self.x) <= cell_size and abs(cell.y - self.y) <= cell_size:
                    return True
        return False