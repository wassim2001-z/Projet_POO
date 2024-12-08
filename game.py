import pygame
from environment import *

# Configuration de l'écran
VIEW_WIDTH = 26  # Nombre de tuiles visibles en largeur
VIEW_HEIGHT = 16  # Nombre de tuiles visibles en hauteur
CELL_SIZE = 60
SCREEN_WIDTH = VIEW_WIDTH * CELL_SIZE
SCREEN_HEIGHT = VIEW_HEIGHT * CELL_SIZE
FPS = 60

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Game Environment")
        self.clock = pygame.time.Clock()
        self.running = True

        # Initialiser l'environnement
        self.environment = Environment(64, 64)  # Carte plus grande
        self.environment.generate_environment(environment_type="mixed")

        # Position de la caméra
        self.camera_x = 0
        self.camera_y = 0

        # Ajouter une unité pour tester le déplacement
        self.unit_x = 5
        self.unit_y = 5

    def handle_input(self):
        """Gère les entrées clavier pour déplacer l'unité."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            if self.unit_y > 0:
                self.unit_y -= 1
        if keys[pygame.K_DOWN]:
            if self.unit_y < self.environment.height - 1:
                self.unit_y += 1
        if keys[pygame.K_LEFT]:
            if self.unit_x > 0:
                self.unit_x -= 1
        if keys[pygame.K_RIGHT]:
            if self.unit_x < self.environment.width - 1:
                self.unit_x += 1

        # Mettre à jour la caméra pour suivre l'unité
        self.camera_x = max(0, min(self.unit_x - VIEW_WIDTH // 2, self.environment.width - VIEW_WIDTH))
        self.camera_y = max(0, min(self.unit_y - VIEW_HEIGHT // 2, self.environment.height - VIEW_HEIGHT))

    def draw(self):
        """Dessine l'environnement et l'unité sur l'écran."""
        self.screen.fill((0, 0, 0))  # Nettoyer l'écran avec une couleur noire
        self.environment.draw_with_camera(self.screen, CELL_SIZE, self.camera_x, self.camera_y, VIEW_WIDTH, VIEW_HEIGHT)

        # Dessiner l'unité
        unit_rect = pygame.Rect(
            (self.unit_x - self.camera_x) * CELL_SIZE,
            (self.unit_y - self.camera_y) * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE
        )
        pygame.draw.rect(self.screen, (255, 0, 0), unit_rect)  # Rouge pour l'unité

        pygame.display.flip()

    def run(self):
        """Boucle principale du jeu."""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.handle_input()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
