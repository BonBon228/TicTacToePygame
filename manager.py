import sys
import pygame
from cloud_database import CloudDatabase
from grid import Grid
from player import Player
from ui import UI

# Set constants for the screen dimensions and color
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_COLOR = (255, 255, 255)

# Class managing the overall game flow
class Manager:
    # Initialize the game, Pygame, and set up the UI, database, and grid
    def __init__(self):
        pygame.init()
        self.cell_size = 40
        self.margin = 0
        self.database = CloudDatabase()
        self.database.save_games_to_json()
        self.ui = UI(SCREEN_WIDTH, SCREEN_HEIGHT, self.database)
        self.grid = Grid(self.ui, SCREEN_WIDTH, SCREEN_HEIGHT, self.cell_size, self.margin)
        symbols = self.ui.main_screen()
        self.grid.draw_grid()
        self.game_over_clicked = False
        self.players = [Player(f'./images/{symbol}.png', symbol, "Player " + str(i + 1)) for i, symbol in enumerate(symbols)]
        self.winner_player = None
        self.current_player_index = 0

    # Switch to the next player in the list
    def switch_player(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    # Check if there is a winner in the game
    def is_has_winner(self):
        return self.winner_player is not None

    # Run the main game loop
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.is_has_winner():
                        self.game_over_clicked = True
                    elif self.grid.click_cell(pygame.mouse.get_pos(), self.players[self.current_player_index]):
                        winning_cells = self.grid.check_win(self.players[self.current_player_index])
                        if winning_cells:
                            self.grid.highlight_cells(winning_cells)
                            self.winner_player = self.players[self.current_player_index]
                            print(f'Player {self.current_player_index + 1} wins!')
                        else:
                            self.switch_player()

            self.ui.update_display()

            if self.is_has_winner() and self.game_over_clicked:
                self.ui.display_winner(self.winner_player, self.players)
                self.__init__()
        
            if self.grid.is_cells_filled() and not self.is_has_winner():
                self.ui.display_winner(self.winner_player, self.players)
                self.__init__()