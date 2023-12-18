import pygame
import sys
import logging
from manager import Manager

# Configure logging to write to a log file
logging.basicConfig(filename='game_logs.log', level=logging.INFO)

# Entry point for the application
if __name__ == "__main__":
    pygame.init()
    
    try:
        logging.info("Initialized succesful!")
        manager = Manager()
        manager.run()
    except Exception as e:
        logging.exception("An exception occurred:")
        print(e)
        pygame.quit()
        sys.exit()