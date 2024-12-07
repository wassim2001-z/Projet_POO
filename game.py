import pygame
from environment import *

# Configuration de l'écran
GRID_WIDTH = 32
GRID_HEIGHT = 16
CELL_SIZE = 60
SCREEN_WIDTH = GRID_WIDTH * CELL_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * CELL_SIZE
FPS = 60

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Game Environment")
        self.clock = pygame.time.Clock()
        self.running = True

        # Initialiser l'environnement
        self.environment = Environment(GRID_WIDTH, GRID_HEIGHT)
        self.environment.generate_environment(environment_type="mixed")

    def draw(self):
        """Dessine l'environnement sur l'écran."""
        self.screen.fill((0, 0, 0))  # Nettoyer l'écran avec une couleur noire
        self.environment.draw(self.screen, CELL_SIZE)
        pygame.display.flip()

    def run(self):
        """Boucle principale du jeu."""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.draw()
            self.clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
