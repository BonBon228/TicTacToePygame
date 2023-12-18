import sys
import pygame


# Class for handling the user interface using Pygame
class UI:
    # Default screen color
    screen_color = (255, 255, 255)

    # Initialize UI with screen dimensions and database connection
    def __init__(self, width, height, database):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.screen.fill(self.screen_color)
        self.database = database

    # Draw a line on the screen
    def draw_line(self, start, end, color):
        pygame.draw.line(self.screen, color, start, end, 2)   

    # Update the display
    def update_display(self):
        pygame.display.update()              

    # Fill the screen with a specified color
    def fill_screen(self, color):
        self.screen.fill(color)

    # Main screen with buttons for playing and viewing game history
    def main_screen(self):
        font = pygame.font.Font(None, 36)
        play_text = font.render("Play", True, (0, 0, 0))
        games_history_text = font.render("Games", True, (0, 0, 0))

        play_button = pygame.Rect(300, 200, 200, 50)
        history_button = pygame.Rect(300, 300, 200, 50)

    
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if play_button.collidepoint(event.pos):
                        return self.players_count_screen()
                    elif history_button.collidepoint(event.pos):
                        self.show_games_history()
    
            pygame.draw.rect(self.screen, (200, 200, 200), play_button)
            pygame.draw.rect(self.screen, (200, 200, 200), history_button)

            self.screen.blit(play_text, (350, 215))
            self.screen.blit(games_history_text, (350, 315))

            pygame.display.flip()

    # Display the game history on the screen
    def show_games_history(self):
        self.fill_screen(self.screen_color)

        font = pygame.font.Font(None, 32)
        y_offset = 50

        games = self.database.get_games()
        if not games:
            no_games_text = "No games are played"
            text_surface = font.render(no_games_text, True, (0, 0, 0))
            self.screen.blit(text_surface, (50, y_offset))
        else:
            for game in games:
                game_data = game.to_dict()
                players = ', '.join([player['name'] for player in game_data['players']])
                winner = game_data['winner']
                game_text = f"Players: {players}, Winner: {winner}"
                text_surface = font.render(game_text, True, (0, 0, 0))
                self.screen.blit(text_surface, (50, y_offset))
                y_offset += 40

        pygame.display.flip()
        waiting_for_close = True
        while waiting_for_close:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    waiting_for_close = False

        self.fill_screen(self.screen_color)

    # Screen for selecting the number of players
    def players_count_screen(self):
        self.fill_screen(self.screen_color)

        font = pygame.font.Font(None, 36)
        text_2_players = font.render("2 Players", True, (0, 0, 0))
        text_3_players = font.render("3 Players", True, (0, 0, 0))
        text_4_players = font.render("4 Players", True, (0, 0, 0))

        button_2_players = pygame.Rect(300, 200, 200, 50)
        button_3_players = pygame.Rect(300, 300, 200, 50)
        button_4_players = pygame.Rect(300, 400, 200, 50)

        pygame.draw.rect(self.screen, (200, 200, 200), button_2_players)
        pygame.draw.rect(self.screen, (200, 200, 200), button_3_players)
        pygame.draw.rect(self.screen, (200, 200, 200), button_4_players)

        self.screen.blit(text_2_players, (350, 215))
        self.screen.blit(text_3_players, (350, 315))
        self.screen.blit(text_4_players, (350, 415))

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if button_2_players.collidepoint(x, y):
                        return ['X', 'O']
                    elif button_3_players.collidepoint(x, y):
                        return ['X', 'O', 'Triangle']
                    elif button_4_players.collidepoint(x, y):
                        return ['X', 'O', 'Triangle', 'Square']
                    
                self.fill_screen(self.screen_color)

    # Display the winner of the game on the screen
    def display_winner(self, winner_player, players):
        self.fill_screen(self.screen_color)

        winner_font = pygame.font.Font(None, 36)
        back_font = pygame.font.Font(None, 32)

        # Check if there is a draw
        if winner_player is None:
            winner_text = winner_font.render("It's a draw", True, (0, 0, 0))
            self.database.add_game(players, "Draw")
        else:
            winner_text = winner_font.render(f"The winner is: {winner_player.name}", True, (0, 0, 0))
            self.database.add_game(players, winner_player.name)

        back_button = pygame.Rect(300, 400, 200, 50)
        pygame.draw.rect(self.screen, (200, 200, 200), back_button)

        back_text = back_font.render("Back to Main Menu", True, (0, 0, 0))
        self.screen.blit(winner_text, (250, 200))
        self.screen.blit(back_text, (300, 415))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if back_button.collidepoint(event.pos):
                        return

            pygame.display.flip()