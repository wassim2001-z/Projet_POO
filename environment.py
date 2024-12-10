import random
import pygame

# Préchargement des textures
def load_textures():
    return {
        "swamp": pygame.image.load("2.png"),
        "forest": pygame.image.load("1.png"),
        "mountain": pygame.image.load("3.png"),
        "obstacle": pygame.image.load("2.png"),
        "plain": pygame.image.load("1.png"),
        "river": pygame.image.load("7.png"),
        "dead_forest": pygame.image.load("6.png"),
        "volcanic": pygame.image.load("4.png"),
        "ruins": pygame.image.load("5.png"),
    }

textures = load_textures()

# Classe Tile
class Tile:
    def __init__(self, x, y, texture_key, visibility=1, speed=1, obstacle=False, special=""):
        self.x = x
        self.y = y
        self.texture = textures[texture_key]
        self.visibility = visibility
        self.speed = speed
        self.obstacle = obstacle
        self.special = special

    def draw(self, screen, cell_size, offset_x, offset_y):
        """Dessine la tuile avec sa texture."""
        rect = pygame.Rect(
            (self.x - offset_x) * cell_size,
            (self.y - offset_y) * cell_size,
            cell_size,
            cell_size
        )
        screen.blit(pygame.transform.scale(self.texture, (cell_size, cell_size)), rect)

class Swamp(Tile):
    def __init__(self, x, y):
        super().__init__(x, y, "swamp", visibility=2, speed=2, obstacle=False, special="swamp")

class Forest(Tile):
    def __init__(self, x, y):
        super().__init__(x, y, "forest", visibility=3, speed=3, obstacle=False, special="dark forest")

class Mountain(Tile):
    def __init__(self, x, y):
        super().__init__(x, y, "mountain", visibility=1, speed=1, obstacle=False, special="mountain")

class Obstacle(Tile):
    def __init__(self, x, y):
        super().__init__(x, y, "obstacle", visibility=0, speed=0, obstacle=True, special="unpassable rock")

class Plain(Tile):
    def __init__(self, x, y):
        super().__init__(x, y, "plain", visibility=4, speed=4, obstacle=False, special="plain")

class River(Tile):
    def __init__(self, x, y):
        super().__init__(x, y, "river", visibility=1, speed=1, obstacle=True, special="river")

class DeadForest(Tile):
    def __init__(self, x, y):
        super().__init__(x, y, "dead_forest", visibility=2, speed=2, obstacle=False, special="dead forest")

class Volcanic(Tile):
    def __init__(self, x, y):
        super().__init__(x, y, "volcanic", visibility=1, speed=1, obstacle=False, special="volcanic")

class Ruins(Tile):
    def __init__(self, x, y):
        super().__init__(x, y, "ruins", visibility=2, speed=1, obstacle=False, special="ruins")

class Environment:
    def __init__(self, width=96, height=96):
        self.width = width
        self.height = height
        self.grid = [[None for _ in range(self.width)] for _ in range(self.height)]

    def is_within_bounds(self, x, y):
        """Check if the given (x, y) coordinates are within the grid boundaries."""
        return 0 <= x < self.width and 0 <= y < self.height

    def is_obstacle(self, x, y):
        """Check if a given tile is an obstacle."""
        if self.is_within_bounds(x, y):
            tile = self.grid[y][x]
            return tile.obstacle if tile else False
        return True

    def generate_environment(self):
        elf_zone = (0, 0, self.width // 2, self.height // 2)
        dwarf_zone = (0, self.height // 2, self.width // 2, self.height)
        human_zone = (self.width // 4, self.height // 4, 3 * self.width // 4, 3 * self.height // 4)
        orc_zone = (self.width // 2, 0, self.width, self.height // 2)
        darkness_zone = (self.width // 2, self.height // 2, self.width, self.height)

        self._fill_zone(elf_zone, forest_pct=0.7, plain_pct=0.1, swamp_pct=0.1, river_pct=0.1)
        self._fill_zone(dwarf_zone, forest_pct=0.1, plain_pct=0.2, mountain_pct=0.6, river_pct=0.1)
        self._fill_zone(human_zone, forest_pct=0.3, plain_pct=0.5, swamp_pct=0.1, river_pct=0.1)
        self._fill_zone(orc_zone, dead_forest_pct=0.3, swamp_pct=0.3, volcanic_pct=0.2, mountain_pct=0.2)
        self._fill_zone(darkness_zone, dead_forest_pct=0.4, ruins_pct=0.3, swamp_pct=0.2, mountain_pct=0.1)

    def _fill_zone(self, zone, forest_pct=0, plain_pct=0, swamp_pct=0, mountain_pct=0, river_pct=0, volcanic_pct=0, dead_forest_pct=0, ruins_pct=0):
        x_start, y_start, x_end, y_end = zone
        num_tiles = (x_end - x_start) * (y_end - y_start)

        num_forest = int(num_tiles * forest_pct)
        num_plain = int(num_tiles * plain_pct)
        num_swamp = int(num_tiles * swamp_pct)
        num_mountain = int(num_tiles * mountain_pct)
        num_river = int(num_tiles * river_pct)
        num_volcanic = int(num_tiles * volcanic_pct)
        num_dead_forest = int(num_tiles * dead_forest_pct)
        num_ruins = int(num_tiles * ruins_pct)

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

        for y in range(y_start, y_end):
            for x in range(x_start, x_end):
                if tiles:
                    tile = tiles.pop()
                    tile.x = x
                    tile.y = y
                    self.grid[y][x] = tile

    def draw_with_camera(self, screen, cell_size, camera_x, camera_y, view_width, view_height):
        for y in range(camera_y, min(camera_y + view_height, self.height)):
            for x in range(camera_x, min(camera_x + view_width, self.width)):
                tile = self.grid[y][x]
                if tile:
                    tile.draw(screen, cell_size, camera_x, camera_y)

    def draw(self, screen, cell_size):
        for y in range(self.height):
            for x in range(self.width):
                tile = self.grid[y][x]
                if tile:
                    tile.draw(screen, cell_size, 0, 0)
