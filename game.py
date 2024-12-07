import pygame
import random

from unit import *
from environment import *

class Game:
    """
    Represents the game.

    Attributes
    ----------
    screen: pygame.Surface
        The game window surface.
    player_units : list[Unit]
        The list of player units.
    enemy_units : list[Unit]
        The list of enemy units.
    grid : list[list[Tile]]
        The grid representing the terrain with different types of tiles.
    """

    def __init__(self, screen):
        """
        Initializes the game with the window surface.

        Parameters
        ----------
        screen : pygame.Surface
            The game window surface.
        """
        self.screen = screen
        self.player_units = [Unit(0, 0, 10, 2, 'player'),
                             Unit(1, 0, 10, 2, 'player')]

        self.enemy_units = [Unit(6, 6, 8, 1, 'enemy'),
                            Unit(7, 6, 8, 1, 'enemy')]

        # Create a grid of tiles (environment)
        self.grid = [
            [Plain(x, y) if (x + y) % 2 == 0 else Forest(x, y) for x in range(WIDTH // CELL_SIZE)]
            for y in range(HEIGHT // CELL_SIZE)
        ]

    def handle_player_turn(self):
        """Player's turn."""
        for selected_unit in self.player_units:
            has_acted = False
            selected_unit.is_selected = True
            self.flip_display()
            while not has_acted:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
      
                    if event.type == pygame.KEYDOWN:
                        dx, dy = 0, 0
                        if event.key == pygame.K_LEFT:
                            dx = -1
                        elif event.key == pygame.K_RIGHT:
                            dx = 1
                        elif event.key == pygame.K_UP:
                            dy = -1
                        elif event.key == pygame.K_DOWN:
                            dy = 1

                        new_x, new_y = selected_unit.x + dx, selected_unit.y + dy
                        if 0 <= new_x < WIDTH // CELL_SIZE and 0 <= new_y < HEIGHT // CELL_SIZE:
                            tile = self.grid[new_y][new_x]
                            if not tile.obstacle:  # Check if the tile is an obstacle
                                selected_unit.move(dx, dy)
                                selected_unit.speed *= tile.speed  # Adjust speed based on the tile
                        self.flip_display()

                        if event.key == pygame.K_SPACE:
                            for enemy in self.enemy_units:
                                if abs(selected_unit.x - enemy.x) <= 1 and abs(selected_unit.y - enemy.y) <= 1:
                                    selected_unit.attack(enemy)
                                    if enemy.health <= 0:
                                        self.enemy_units.remove(enemy)
                            has_acted = True
                            selected_unit.is_selected = False

    def handle_enemy_turn(self):
        """Simple AI for enemy units."""
        for enemy in self.enemy_units:
            target = random.choice(self.player_units)
            dx = 1 if enemy.x < target.x else -1 if enemy.x > target.x else 0
            dy = 1 if enemy.y < target.y else -1 if enemy.y > target.y else 0
            enemy.move(dx, dy)

            if abs(enemy.x - target.x) <= 1 and abs(enemy.y - target.y) <= 1:
                enemy.attack(target)
                if target.health <= 0:
                    self.player_units.remove(target)

    def flip_display(self):
        """Displays the game."""
        self.screen.fill(BLACK)
        for row in self.grid:
            for tile in row:
                tile.draw(self.screen, CELL_SIZE)

        for unit in self.player_units + self.enemy_units:
            unit.draw(self.screen)

        pygame.display.flip()


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Strategy Game")

    game = Game(screen)

    while True:
        game.handle_player_turn()
        game.handle_enemy_turn()


if __name__ == "__main__":
    main()
