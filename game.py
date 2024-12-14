import pygame
import random
from environment import Environment
from unit import Elf, Human, Orc, Dwarf, Goblin, Troll, Weapon, HealthPotion
from smoke import Smoke
from interface import Interface

# Constantes
GRID_WIDTH = 96
GRID_HEIGHT = 96
CELL_SIZE = 60
VIEW_WIDTH = 26
VIEW_HEIGHT = 16
SIDEBAR_WIDTH = 300
SCREEN_WIDTH = VIEW_WIDTH * CELL_SIZE + SIDEBAR_WIDTH
SCREEN_HEIGHT = VIEW_HEIGHT * CELL_SIZE
FPS = 30

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Turn-Based Combat Game with Items")
        self.clock = pygame.time.Clock()

        # Environment setup
        self.environment = Environment(GRID_WIDTH, GRID_HEIGHT)
        self.environment.generate_environment()

        # Ajouter les unités
        self.units = [
            Elf(GRID_WIDTH // 2, GRID_HEIGHT // 2),
            Human(GRID_WIDTH // 2 + 3, GRID_HEIGHT // 2 + 3),
            Orc(GRID_WIDTH // 2 - 3, GRID_HEIGHT // 2 - 3)
        ]
        self.current_unit_index = 0
        self.turn_counter = 0  # Compteur pour la régénération des points de compétence
        self.game_over = False
 
        # Interface setup
        self.interface = Interface(width=SIDEBAR_WIDTH)

        # Objets et effets
        self.weapons = []
        self.health_potions = []
        self.smoke_effect = None  # Effet de fumée

        # Générer objets
        self.generate_weapons(10)
        self.generate_health_potions(10)

        # Initialiser la sélection et la caméra
        self.camera_x = self.units[0].x - VIEW_WIDTH // 2
        self.camera_y = self.units[0].y - VIEW_HEIGHT // 2
        self.selected_tile = (self.units[0].x, self.units[0].y)
        self.accessible_tiles = []  # Tuiles accessibles

    def generate_weapons(self, num_weapons):
        for _ in range(num_weapons):
            while True:
                x = random.randint(0, GRID_WIDTH - 1)
                y = random.randint(0, GRID_HEIGHT - 1)
                if not self.environment.is_obstacle(x, y):
                    self.weapons.append(Weapon(x, y))
                    break

    def generate_health_potions(self, num_potions):
        for _ in range(num_potions):
            while True:
                x = random.randint(0, GRID_WIDTH - 1)
                y = random.randint(0, GRID_HEIGHT - 1)
                if not self.environment.is_obstacle(x, y):
                    self.health_potions.append(HealthPotion(x, y))
                    break

    def calculate_accessible_tiles(self):
        """Calcule les tuiles accessibles pour l'unité actuelle."""
        current_unit = self.units[self.current_unit_index]
        self.accessible_tiles = []
        for dy in range(-current_unit.speed, current_unit.speed + 1):
            for dx in range(-current_unit.speed, current_unit.speed + 1):
                new_x = current_unit.x + dx
                new_y = current_unit.y + dy
                if abs(dx) + abs(dy) <= current_unit.speed and self.environment.is_within_bounds(new_x, new_y):
                    tile = self.environment.grid[new_y][new_x]
                    if tile and not tile.obstacle:
                        self.accessible_tiles.append((new_x, new_y))

    def handle_input(self):
        if self.game_over:
            return

        current_unit = self.units[self.current_unit_index]
        keys = pygame.key.get_pressed()

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

        if (new_x, new_y) in self.accessible_tiles:
            self.selected_tile = (new_x, new_y)

        # Déplacement
        if keys[pygame.K_RETURN]:
            if self.selected_tile in self.accessible_tiles:
                current_unit.x, current_unit.y = self.selected_tile
                self.check_for_item(current_unit)
                self.end_turn()

        # Attaque
        if keys[pygame.K_a]:
            target = self.get_unit_at(self.selected_tile)
            if target and target != current_unit:
                current_unit.attack(target)
                self.interface.add_message("attack", unit_type=current_unit.unit_type, value=current_unit.attack_power)
                self.check_game_status()
                self.end_turn()

        # Utilisation des compétences
        if keys[pygame.K_1]:
            skill_name = current_unit.use_skill(1)
            if skill_name:
                self.interface.add_message("skill", unit_type=current_unit.unit_type, skill_name=skill_name)
                self.end_turn()
        if keys[pygame.K_2]:
            skill_name = current_unit.use_skill(2)
            if skill_name:
                self.interface.add_message("skill", unit_type=current_unit.unit_type, skill_name=skill_name)
                self.end_turn()
        if keys[pygame.K_3]:
            skill_name = current_unit.use_skill(3)
            if skill_name:
                self.interface.add_message("skill", unit_type=current_unit.unit_type, skill_name=skill_name)
                self.end_turn()

        # Gestion de la caméra
        self.camera_x = current_unit.x - VIEW_WIDTH // 2
        self.camera_y = current_unit.y - VIEW_HEIGHT // 2
        self.camera_x = max(0, min(self.camera_x, GRID_WIDTH - VIEW_WIDTH))
        self.camera_y = max(0, min(self.camera_y, GRID_HEIGHT - VIEW_HEIGHT))

    def check_for_item(self, unit):
        """Vérifie si une unité est sur une case contenant un objet et applique l'effet."""
        for weapon in self.weapons:
            if weapon.x == unit.x and weapon.y == unit.y:
                unit.pick_up_weapon(weapon)
                self.interface.add_message("attack", unit_type=unit.unit_type, value=weapon.attack_boost)
                self.weapons.remove(weapon)
                break

        for potion in self.health_potions:
            if potion.x == unit.x and potion.y == unit.y:
                unit.health = min(100, unit.health + potion.health_boost)
                self.interface.add_message("skill", unit_type=unit.unit_type, skill_name="Health Potion")
                self.health_potions.remove(potion)
                break

    def get_unit_at(self, position):
        for unit in self.units:
            if (unit.x, unit.y) == position:
                return unit
        return None

    def end_turn(self):
        if self.game_over:
            return

        self.current_unit_index = (self.current_unit_index + 1) % len(self.units)
        self.selected_tile = (self.units[self.current_unit_index].x, self.units[self.current_unit_index].y)
        self.calculate_accessible_tiles()
        self.turn_counter += 1

        if self.turn_counter % 3 == 0:
            for unit in self.units:
                unit.update_skill_points()

    def check_game_status(self):
        allies = [unit for unit in self.units if isinstance(unit, (Elf, Human, Dwarf))]
        enemies = [unit for unit in self.units if isinstance(unit, (Orc, Goblin, Troll))]

        if all(unit.health <= 0 for unit in allies):
            self.interface.add_message("skill", unit_type="Game", skill_name="Defeat")
            self.game_over = True

        if all(unit.health <= 0 for unit in enemies):
            self.interface.add_message("skill", unit_type="Game", skill_name="Victory")
            self.game_over = True

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.environment.draw_with_camera(self.screen, CELL_SIZE, self.camera_x, self.camera_y, VIEW_WIDTH, VIEW_HEIGHT)

        # Dessiner les tuiles accessibles
        for tile in self.accessible_tiles:
            screen_x = (tile[0] - self.camera_x) * CELL_SIZE
            screen_y = (tile[1] - self.camera_y) * CELL_SIZE
            pygame.draw.rect(self.screen, (0, 255, 0, 100), (screen_x, screen_y, CELL_SIZE, CELL_SIZE), 2)

        # Dessiner la tuile sélectionnée
        selected_x = (self.selected_tile[0] - self.camera_x) * CELL_SIZE
        selected_y = (self.selected_tile[1] - self.camera_y) * CELL_SIZE
        pygame.draw.rect(self.screen, (255, 255, 0), (selected_x, selected_y, CELL_SIZE, CELL_SIZE), 3)

        for weapon in self.weapons:
            weapon.draw(self.screen, (weapon.x - self.camera_x) * CELL_SIZE, (weapon.y - self.camera_y) * CELL_SIZE)

        for potion in self.health_potions:
            potion.draw(self.screen, (potion.x - self.camera_x) * CELL_SIZE, (potion.y - self.camera_y) * CELL_SIZE)

        for unit in self.units:
            unit.draw(self.screen, (unit.x - self.camera_x) * CELL_SIZE, (unit.y - self.camera_y) * CELL_SIZE)

        if self.smoke_effect:
            self.smoke_effect.draw(self.screen, self.camera_x, self.camera_y, CELL_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT)

        # Dessiner l'interface
        self.interface.draw(self.screen, self.units)

        pygame.display.flip()

    def run(self):
        self.calculate_accessible_tiles()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if self.smoke_effect:
                self.smoke_effect.duration -= 1
                if self.smoke_effect.duration <= 0:
                    self.smoke_effect = None

            self.handle_input()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
