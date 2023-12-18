import pygame


# Class representing a player in the game
class Player:
    # Initialize a player with an image path, symbol, and name
    def __init__(self, image_path, symbol, name):
        self.image_symbol = pygame.image.load(image_path)
        self.symbol = symbol
        self.name = name

    # Convert player information to a dictionary
    def to_dict(self):
        return {
            'name': self.name,
        }