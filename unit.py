import pygame
import random
from environment import *
# Constantes
GRID_SIZE = 16
CELL_SIZE = 60
WIDTH = 2*GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)




class Unit:
    """Base class for all units."""
    def __init__(self, x, y, health, attack_power, speed, environment):
        self.x = x
        self.y = y
        self.health = health
        self.attack_power = attack_power
        self.speed = speed
        self.environment = environment
        self.image = None  # Placeholder for the unit image
        self.unit_type = "Generic Unit"

    def load_image(self, image_path):
        """Loads an image for the unit using pygame."""
        try:
            self.image = pygame.image.load(image_path).convert_alpha()
        except pygame.error as e:
            print(f"Error loading image {image_path}: {e}")

    def draw(self, screen):
        """Draws the unit on the screen with a health bar."""
        if self.image:
            screen.blit(self.image, (self.x * CELL_SIZE, self.y * CELL_SIZE))
        # Draw health bar
        health_bar_width = CELL_SIZE
        health_ratio = self.health / 100  # Assuming max health is 100 for simplicity
        health_bar_height = 5
        health_bar_color = (255, 0, 0)  # Red for health
        pygame.draw.rect(screen, health_bar_color, (self.x * CELL_SIZE, self.y * CELL_SIZE - health_bar_height, health_bar_width * health_ratio, health_bar_height))

class Human(Unit):
    """Human unit."""
    def __init__(self, x, y):
        super().__init__(x, y, health=100, attack_power=15, speed=3, environment="plain")
        self.unit_type = "Human"
        self.load_image("images/human.png")  # Load image for the Human unit
 
    def environment_advantage(self, tile):
        if isinstance(tile, Plain):
            self.speed += 1  # Bonus de vitesse sur les plaines

    def special_ability(self):
        pass  # La capacité spéciale sera définie plus tard

  
class Elf(Unit):
    """Elf unit."""
    def __init__(self, x, y):
        super().__init__(x, y, health=80, attack_power=20, speed=4, environment="forest")
        self.unit_type = "Elf"
        self.load_image("images/elf.png")  # Load image for the Elf unit

    def environment_advantage(self, tile):
        if isinstance(tile, Forest):
            self.attack_power += 5  # Bonus d'attaque dans la forêt

    def special_ability(self):
        pass  # La capacité spéciale sera définie plus tard


class Dwarf(Unit):
    """Dwarf unit."""
    def __init__(self, x, y):
        super().__init__(x, y, health=120, attack_power=10, speed=2, environment="mountain")
        self.unit_type = "Dwarf"
        self.load_image("images/dwarf.png")  # Load image for the Dwarf unit

    def environment_advantage(self, tile):
        if isinstance(tile, Mountain):
            self.health += 10  # Bonus de santé dans les montagnes

    def special_ability(self):
        pass  # La capacité spéciale sera définie plus tard


class Orc(Unit):
    """Orc unit."""
    def __init__(self, x, y):
        super().__init__(x, y, health=90, attack_power=18, speed=3, environment="swamp")
        self.unit_type = "Orc"
        self.load_image("images/orc.png")  # Load image for the Orc unit

    def environment_advantage(self, tile):
        if isinstance(tile, Swamp):
            self.attack_power += 3  # Bonus d'attaque dans les marécages

    def special_ability(self):
        pass  # La capacité spéciale sera définie plus tard


class Goblin(Unit):
    """Goblin unit."""
    def __init__(self, x, y):
        super().__init__(x, y, health=60, attack_power=12, speed=4, environment="obstacle")
        self.unit_type = "Goblin"
        self.load_image("images/goblin.png")  # Load image for the Goblin unit

    def environment_advantage(self, tile):
        if isinstance(tile, Obstacle):
            self.speed += 1  # Bonus de vitesse sur les obstacles

    def special_ability(self):
        pass  # La capacité spéciale sera définie plus tard


class Troll(Unit):
    """Troll unit."""
    def __init__(self, x, y):
        super().__init__(x, y, health=150, attack_power=25, speed=2, environment="mixed")
        self.unit_type = "Troll"
        self.load_image("images/troll.png")  # Load image for the Troll unit

    def environment_advantage(self, tile):
        if isinstance(tile, Mountain) or isinstance(tile, Swamp):
            self.health += 5  # Régénération lente sur les montagnes ou marécages

    def special_ability(self):
        pass  # La capacité spéciale sera définie plus tard
