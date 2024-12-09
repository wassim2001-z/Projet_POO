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

        # Initialiser la caméra
        self.camera_x = self.player_unit.x - VIEW_WIDTH // 2
        self.camera_y = self.player_unit.y - VIEW_HEIGHT // 2

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.player_unit.y > 0:
            self.player_unit.y -= 1
        if keys[pygame.K_DOWN] and self.player_unit.y < GRID_HEIGHT - 1:
            self.player_unit.y += 1
        if keys[pygame.K_LEFT] and self.player_unit.x > 0:
            self.player_unit.x -= 1
        if keys[pygame.K_RIGHT] and self.player_unit.x < GRID_WIDTH - 1:
            self.player_unit.x += 1

        self.camera_x = self.player_unit.x - VIEW_WIDTH // 2
        self.camera_y = self.player_unit.y - VIEW_HEIGHT // 2
        self.camera_x = max(0, min(self.camera_x, GRID_WIDTH - VIEW_WIDTH))
        self.camera_y = max(0, min(self.camera_y, GRID_HEIGHT - VIEW_HEIGHT))

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.environment.draw_with_camera(self.screen, CELL_SIZE, self.camera_x, self.camera_y, VIEW_WIDTH, VIEW_HEIGHT)

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
