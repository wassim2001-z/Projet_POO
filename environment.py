import random
import pygame

# Classe Tile
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

    def draw(self, screen, cell_size, offset_x, offset_y):
        """Draws the tile on the screen, adjusted for camera offset."""
        rect = pygame.Rect(
            (self.x - offset_x) * cell_size,
            (self.y - offset_y) * cell_size,
            cell_size,
            cell_size
        )
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

class River(Tile):
    """River tile."""
    def __init__(self, x, y):
        super().__init__(x, y, color=(0, 102, 204), visibility=1, speed=1, obstacle=True, special="river")

class DeadForest(Tile):
    """Dead forest tile."""
    def __init__(self, x, y):
        super().__init__(x, y, color=(60, 40, 20), visibility=2, speed=2, obstacle=False, special="dead forest")

class Volcanic(Tile):
    """Volcanic tile."""
    def __init__(self, x, y):
        super().__init__(x, y, color=(153, 0, 0), visibility=1, speed=1, obstacle=False, special="volcanic")

class Ruins(Tile):
    """Ruins tile."""
    def __init__(self, x, y):
        super().__init__(x, y, color=(100, 100, 100), visibility=2, speed=1, obstacle=False, special="ruins")

class Environment:
    """
    Represents the environment generator for the game board.
    """
    def __init__(self, width=96, height=96):
        self.width = width
        self.height = height
        self.grid = [[None for _ in range(self.width)] for _ in range(self.height)]

    def generate_environment(self):
        """
        Generates a large map divided into regions for each faction, with flexibility to specify types.
        """
        # Define the zones
        elf_zone = (0, 0, self.width // 2, self.height // 2)
        dwarf_zone = (0, self.height // 2, self.width // 2, self.height)
        human_zone = (self.width // 4, self.height // 4, 3 * self.width // 4, 3 * self.height // 4)
        orc_zone = (self.width // 2, 0, self.width, self.height // 2)
        darkness_zone = (self.width // 2, self.height // 2, self.width, self.height)

        # Fill each zone
        self._fill_zone(elf_zone, forest_pct=0.7, plain_pct=0.1, swamp_pct=0.1, river_pct=0.1)
        self._fill_zone(dwarf_zone, forest_pct=0.1, plain_pct=0.2, mountain_pct=0.6, river_pct=0.1)
        self._fill_zone(human_zone, forest_pct=0.3, plain_pct=0.5, swamp_pct=0.1, river_pct=0.1)
        self._fill_zone(orc_zone, dead_forest_pct=0.3, swamp_pct=0.3, volcanic_pct=0.2, mountain_pct=0.2)
        self._fill_zone(darkness_zone, dead_forest_pct=0.4, ruins_pct=0.3, swamp_pct=0.2, mountain_pct=0.1)

    def _fill_zone(self, zone, forest_pct=0, plain_pct=0, swamp_pct=0, mountain_pct=0, river_pct=0, volcanic_pct=0, dead_forest_pct=0, ruins_pct=0):
        """Fills a specific zone with tiles based on given percentages."""
        x_start, y_start, x_end, y_end = zone
        num_tiles = (x_end - x_start) * (y_end - y_start)

        # Calculate the number of tiles for each type
        num_forest = int(num_tiles * forest_pct)
        num_plain = int(num_tiles * plain_pct)
        num_swamp = int(num_tiles * swamp_pct)
        num_mountain = int(num_tiles * mountain_pct)
        num_river = int(num_tiles * river_pct)
        num_volcanic = int(num_tiles * volcanic_pct)
        num_dead_forest = int(num_tiles * dead_forest_pct)
        num_ruins = int(num_tiles * ruins_pct)

        # Create tiles list
        tiles = (
            [Forest(0, 0) for _ in range(num_forest)] +
            [Plain(0, 0) for _ in range(num_plain)] +
            [Swamp(0, 0) for _ in range(num_swamp)] +
            [Mountain(0, 0) for _ in range(num_mountain)] +
            [River(0, 0) for _ in range(num_river)] +
            [Volcanic(0, 0) for _ in range(num_volcanic)] +
            [DeadForest(0, 0) for _ in range(num_dead_forest)] +
            [Ruins(0, 0) for _ in range(num_ruins)]
        )
        random.shuffle(tiles)

        # Fill the grid within the zone
        for y in range(y_start, y_end):
            for x in range(x_start, x_end):
                if tiles:
                    tile = tiles.pop()
                    tile.x = x
                    tile.y = y
                    self.grid[y][x] = tile

    def draw_with_camera(self, screen, cell_size, camera_x, camera_y, view_width, view_height):
        """Draws the environment based on the camera's current position."""
        for y in range(camera_y, min(camera_y + view_height, self.height)):
            for x in range(camera_x, min(camera_x + view_width, self.width)):
                tile = self.grid[y][x]
                if tile:
                    tile.draw(screen, cell_size, camera_x, camera_y)

    def draw(self, screen, cell_size):
        """Draws the entire environment on the screen."""
        for y in range(self.height):
            for x in range(self.width):
                tile = self.grid[y][x]
                if tile:
                    tile.draw(screen, cell_size, 0, 0)
