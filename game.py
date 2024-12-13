import pygame
from environment import Environment
from unit import Elf, Human, Orc, Dwarf, Goblin, Troll

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
        pygame.display.set_caption("Turn-Based Combat Game")
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
        self.turn_counter = 0  # Compteur pour gérer la régénération des points de compétence
        self.game_over = False

        # Initialiser la sélection et la caméra
        self.camera_x = self.units[0].x - VIEW_WIDTH // 2
        self.camera_y = self.units[0].y - VIEW_HEIGHT // 2
        self.selected_tile = (self.units[0].x, self.units[0].y)

    def handle_input(self):
        if self.game_over:
            return

        current_unit = self.units[self.current_unit_index]
        keys = pygame.key.get_pressed()
        movement_range = current_unit.speed

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

        # Calculer la distance du déplacement
        distance = abs(new_x - current_unit.x) + abs(new_y - current_unit.y)

        # Mise à jour de la sélection si valide
        if distance <= movement_range and self.environment.is_within_bounds(new_x, new_y) and not self.environment.is_obstacle(new_x, new_y):
            self.selected_tile = (new_x, new_y)

        # Valider le déplacement
        if keys[pygame.K_RETURN]:
            current_unit.x, current_unit.y = self.selected_tile
            self.end_turn()

        # Attaquer une unité ennemie
        if keys[pygame.K_a]:
            target = self.get_unit_at(self.selected_tile)
            if target and target != current_unit:
                current_unit.attack(target)
                self.check_game_status()
                self.end_turn()

        # Utiliser une compétence avec 1, 2 ou 3
        if keys[pygame.K_1]:
            if current_unit.use_skill(1):
                self.end_turn()
        if keys[pygame.K_2]:
            if current_unit.use_skill(2):
                self.end_turn()
        if keys[pygame.K_3]:
            if current_unit.use_skill(3):
                self.end_turn()

        # Mise à jour de la caméra
        self.camera_x = current_unit.x - VIEW_WIDTH // 2
        self.camera_y = current_unit.y - VIEW_HEIGHT // 2
        self.camera_x = max(0, min(self.camera_x, GRID_WIDTH - VIEW_WIDTH))
        self.camera_y = max(0, min(self.camera_y, GRID_HEIGHT - VIEW_HEIGHT))

    def get_unit_at(self, position):
        for unit in self.units:
            if (unit.x, unit.y) == position:
                return unit
        return None

    def end_turn(self):
        if self.game_over:
            return

        # Passer au prochain tour
        self.current_unit_index = (self.current_unit_index + 1) % len(self.units)
        self.selected_tile = (self.units[self.current_unit_index].x, self.units[self.current_unit_index].y)
        
        # Incrémenter le compteur de tours
        self.turn_counter += 1

        # Mise à jour des points de compétence toutes les 3 tours
        if self.turn_counter % 3 == 0:
            for unit in self.units:
                unit.update_skill_points()

    def check_game_status(self):
        """Check the victory or defeat conditions."""
        allies = [unit for unit in self.units if isinstance(unit, (Elf, Human, Dwarf))]
        enemies = [unit for unit in self.units if isinstance(unit, (Orc, Goblin, Troll))]

        if all(unit.health <= 0 for unit in allies):
            print("Defeat! All allied units have been defeated.")
            self.game_over = True

        if all(unit.health <= 0 for unit in enemies):
            print("Victory! All enemy units have been defeated.")
            self.game_over = True

    def draw_accessible_tiles(self):
        current_unit = self.units[self.current_unit_index]
        movement_range = current_unit.speed
        for y in range(max(0, current_unit.y - movement_range), min(GRID_HEIGHT, current_unit.y + movement_range + 1)):
            for x in range(max(0, current_unit.x - movement_range), min(GRID_WIDTH, current_unit.x + movement_range + 1)):
                if abs(x - current_unit.x) + abs(y - current_unit.y) <= movement_range and not self.environment.is_obstacle(x, y):
                    screen_x = (x - self.camera_x) * CELL_SIZE
                    screen_y = (y - self.camera_y) * CELL_SIZE
                    color = (0, 0, 255, 100) if (x, y) == self.selected_tile else (0, 255, 0, 100)
                    pygame.draw.rect(self.screen, color, (screen_x, screen_y, CELL_SIZE, CELL_SIZE), 2)

    def draw_units(self):
        for unit in self.units:
            player_screen_x = (unit.x - self.camera_x) * CELL_SIZE
            player_screen_y = (unit.y - self.camera_y) * CELL_SIZE
            unit.draw(self.screen, player_screen_x, player_screen_y)

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.environment.draw_with_camera(self.screen, CELL_SIZE, self.camera_x, self.camera_y, VIEW_WIDTH, VIEW_HEIGHT)

        # Dessiner les cases accessibles
        self.draw_accessible_tiles()

        # Dessiner les unités
        self.draw_units()

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
