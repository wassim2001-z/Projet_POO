import pygame
from environment import Environment
from unit import Elf

# Constantes
GRID_WIDTH = 96
GRID_HEIGHT = 96
CELL_SIZE = 60
VIEW_WIDTH = 26
VIEW_HEIGHT = 16
SCREEN_WIDTH = VIEW_WIDTH * CELL_SIZE
SCREEN_HEIGHT = VIEW_HEIGHT * CELL_SIZE
FPS = 30

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Dynamic Map with Camera")
        self.clock = pygame.time.Clock()

        # Environment setup
        self.environment = Environment(GRID_WIDTH, GRID_HEIGHT)
        self.environment.generate_environment()

        # Ajouter les unités
        self.player_unit = Elf(GRID_WIDTH // 2, GRID_HEIGHT // 2)

        # Initialiser la sélection et la caméra
        self.camera_x = self.player_unit.x - VIEW_WIDTH // 2
        self.camera_y = self.player_unit.y - VIEW_HEIGHT // 2
        self.selected_tile = (self.player_unit.x, self.player_unit.y)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        accessible_tiles = self.player_unit.get_accessible_tiles(self.environment)

        # Navigation de la sélection
        new_x, new_y = self.selected_tile
        if keys[pygame.K_UP]:
            new_y -= 1
        if keys[pygame.K_DOWN]:
            new_y += 1
        if keys[pygame.K_LEFT]:
            new_x -= 1
        if keys[pygame.K_RIGHT]:
            new_x += 1

        # Mise à jour de la sélection si valide
        if (new_x, new_y) in accessible_tiles:
            self.selected_tile = (new_x, new_y)

        # Valider le déplacement
        if keys[pygame.K_RETURN]:
            if self.selected_tile in accessible_tiles:
                self.player_unit.x, self.player_unit.y = self.selected_tile
                # Réinitialiser la sélection sur l'unité
                self.selected_tile = (self.player_unit.x, self.player_unit.y)

        # Mise à jour de la caméra
        self.camera_x = self.player_unit.x - VIEW_WIDTH // 2
        self.camera_y = self.player_unit.y - VIEW_HEIGHT // 2
        self.camera_x = max(0, min(self.camera_x, GRID_WIDTH - VIEW_WIDTH))
        self.camera_y = max(0, min(self.camera_y, GRID_HEIGHT - VIEW_HEIGHT))

    def draw_accessible_tiles(self):
        accessible_tiles = self.player_unit.get_accessible_tiles(self.environment)

        for tile_x, tile_y in accessible_tiles:
            screen_x = (tile_x - self.camera_x) * CELL_SIZE
            screen_y = (tile_y - self.camera_y) * CELL_SIZE
            color = (0, 0, 255, 100) if (tile_x, tile_y) == self.selected_tile else (0, 255, 0, 100)
            pygame.draw.rect(self.screen, color, (screen_x, screen_y, CELL_SIZE, CELL_SIZE), 2)

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.environment.draw_with_camera(self.screen, CELL_SIZE, self.camera_x, self.camera_y, VIEW_WIDTH, VIEW_HEIGHT)

        # Dessiner les cases accessibles
        self.draw_accessible_tiles()

        # Dessiner l'unité
        player_screen_x = (self.player_unit.x - self.camera_x) * CELL_SIZE
        player_screen_y = (self.player_unit.y - self.camera_y) * CELL_SIZE
        self.player_unit.draw(self.screen, player_screen_x, player_screen_y)

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.handle_input()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
