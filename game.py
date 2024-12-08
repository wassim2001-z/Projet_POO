import pygame
from environment import Environment

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

        # Camera setup
        self.camera_x = 0
        self.camera_y = 0

        # Player position
        self.player_x = GRID_WIDTH // 2
        self.player_y = GRID_HEIGHT // 2

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.player_y > 0:
            self.player_y -= 1
        if keys[pygame.K_DOWN] and self.player_y < GRID_HEIGHT - 1:
            self.player_y += 1
        if keys[pygame.K_LEFT] and self.player_x > 0:
            self.player_x -= 1
        if keys[pygame.K_RIGHT] and self.player_x < GRID_WIDTH - 1:
            self.player_x += 1

        # Update camera position to follow the player
        self.camera_x = max(0, min(self.player_x - VIEW_WIDTH // 2, GRID_WIDTH - VIEW_WIDTH))
        self.camera_y = max(0, min(self.player_y - VIEW_HEIGHT // 2, GRID_HEIGHT - VIEW_HEIGHT))

    def draw(self):
        self.screen.fill((0, 0, 0))

        # Draw the environment with the camera
        self.environment.draw_with_camera(self.screen, CELL_SIZE, self.camera_x, self.camera_y, VIEW_WIDTH, VIEW_HEIGHT)

        # Draw the player
        player_rect = pygame.Rect(
            (self.player_x - self.camera_x) * CELL_SIZE,
            (self.player_y - self.camera_y) * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE
        )
        pygame.draw.rect(self.screen, (255, 0, 0), player_rect)

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
