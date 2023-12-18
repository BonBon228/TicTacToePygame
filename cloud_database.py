import json
import firebase_admin
from firebase_admin import credentials, firestore


# Initialize Firebase with the provided credentials
cred = credentials.Certificate("accountKey.json")
firebase_admin.initialize_app(cred)

# Class for interacting with the Firebase Cloud Firestore database
class CloudDatabase:
    def __init__(self):
        # Initialize Firestore client
        self.db = firestore.client()
        # Reference to the 'games' collection in Firestore
        self.games_ref =self.db.collection('games').document()

    # Add a game record to the 'games' collection
    def add_game(self, players, winner):
        players_data = [player.to_dict() for player in players]
        self.games_ref.set({
            'players': players_data,
            'winner': winner,
        })

    # Retrieve all games from the 'games' collection
    def get_games(self):
        return self.db.collection('games').get()
    
    # Save game data to a JSON file
    def save_games_to_json(self):
        games = self.get_games()
        games_data = [game.to_dict() for game in games]
        with open('games.json', 'w') as f:
            json.dump(games_data, f, indent=4, separators=(',', ': '))