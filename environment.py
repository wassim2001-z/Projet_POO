import pygame
import random
from unit import *

class Tile:
    """
    Represents a tile on the game board.

    Attributes
    ----------
    x, y : int Position of the tile on the grid.
    color : tuple Color of the tile.
    visibility : int Visibility level (between 1 and 4).
    speed : int Speed factor (integer to increase or decrease the speed of the unit).
    obstacle : bool Indicates if the tile is an obstacle.
    special : str Special attribute for unique characteristics of the tile.
    """

    def __init__(self, x, y, color=(255, 255, 255), visibility=1, speed=1, obstacle=False, special=""):
        self.x = x
        self.y = y
        self.color = color
        self.visibility = visibility
        self.speed = speed
        self.obstacle = obstacle
        self.special = special

 
    def draw(self, screen, cell_size):
        """Draws the tile on the screen."""
        rect = pygame.Rect(self.x * cell_size, self.y * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, self.color, rect)


class Swamp(Tile):
    """Water tile (swamp)."""
    def __init__(self, x, y):
        super().__init__(x, y, color=(0, 51, 102), visibility=2, speed=2, obstacle=False, special="swamp")


class Forest(Tile):
    """Forest tile (dark forest)."""
    def __init__(self, x, y):
        super().__init__(x, y, color=(0, 50, 0), visibility=3, speed=3, obstacle=False, special="dark forest")


class Mountain(Tile):
    """Mountain tile (dark)."""
    def __init__(self, x, y):
        super().__init__(x, y, color=(50, 50, 50), visibility=1, speed=1, obstacle=False, special="mountain")


class Obstacle(Tile):
    """Unpassable obstacle tile."""
    def __init__(self, x, y):
        super().__init__(x, y, color=(30, 30, 30), visibility=0, speed=0, obstacle=True, special="unpassable rock")


class Plain(Tile):
    """Plain tile (flat and open land)."""
    def __init__(self, x, y):
        super().__init__(x, y, color=(140, 180, 120), visibility=4, speed=4, obstacle=False, special="plain")


class Environment:
    """
    Represents the environment generator for the game board.
    """
    def __init__(self, width=32, height=16):
        self.width = width
        self.height = height
        self.grid = [[None for _ in range(self.width)] for _ in range(self.height)]

    def generate_environment(self, environment_type="mixed"):
        """
        Generates an environment based on the given type.

        Parameters
        ----------
        environment_type : str
            Type of environment to generate ("dark_forest", "high_mountain", "plain", "swamp_obstacle", "mixed").
        """
        num_tiles = self.width * self.height

        # Define the percentage distribution for each environment type
        if environment_type == "dark_forest":
            forest_pct, mountain_pct, obstacle_pct, swamp_pct = 0.60, 0.10, 0.10, 0.10
        elif environment_type == "high_mountain":
            forest_pct, mountain_pct, obstacle_pct, swamp_pct = 0.05, 0.50, 0.15, 0.10
        elif environment_type == "plain":
            forest_pct, mountain_pct, obstacle_pct, swamp_pct = 0.20, 0.05, 0.10, 0.05
        elif environment_type == "swamp_obstacle":
            forest_pct, mountain_pct, obstacle_pct, swamp_pct = 0.20, 0.15, 0.25, 0.30
        else:  # mixed
            forest_pct, mountain_pct, obstacle_pct, swamp_pct = 0.35, 0.20, 0.15, 0.15

        plain_pct = 1.0 - (forest_pct + mountain_pct + obstacle_pct + swamp_pct)

        # Calculate the number of tiles for each type
        num_forest = int(num_tiles * forest_pct)
        num_mountain = int(num_tiles * mountain_pct)
        num_obstacle = int(num_tiles * obstacle_pct)
        num_swamp = int(num_tiles * swamp_pct)
        num_plain = num_tiles - (num_forest + num_mountain + num_obstacle + num_swamp)

        # Create tiles list
        tiles = (
            [Forest(0, 0) for _ in range(num_forest)] +
            [Mountain(0, 0) for _ in range(num_mountain)] +
            [Obstacle(0, 0) for _ in range(num_obstacle)] +
            [Swamp(0, 0) for _ in range(num_swamp)] +
            [Plain(0, 0) for _ in range(num_plain)]
        )
        random.shuffle(tiles)

        # Fill the grid with shuffled tiles
        for y in range(self.height):
            for x in range(self.width):
                tile = tiles.pop()
                tile.x = x
                tile.y = y
                self.grid[y][x] = tile

    def draw(self, screen, cell_size):
        """Draws the environment on the screen."""
        for row in self.grid:
            for tile in row:
                tile.draw(screen, cell_size)


def main():
    pygame.init()
    screen_width, screen_height = WIDTH, HEIGHT
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Environment Generation Example")

    cell_size = CELL_SIZE  # Use cell size defined in the unit file
    environment = Environment()
    environment.generate_environment(environment_type="plain")

    clock = pygame.time.Clock()
    running = True
    while running:
        screen.fill((0, 0, 0))
        environment.draw(screen, cell_size)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
