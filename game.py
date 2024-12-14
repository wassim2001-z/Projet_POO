<<<<<<< HEAD
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
=======
import pygame
import random
from environment import Environment
from unit import Elf
from unit import Weapon
from unit import HealthPotion
from smoke import Smoke

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

        # 添加武器和药水
        self.weapons = []
        self.health_potions = []
        self.generate_weapons(20)
        self.generate_health_potions(20)

 
        # Initialiser la sélection et la caméra
        self.camera_x = self.player_unit.x - VIEW_WIDTH // 2
        self.camera_y = self.player_unit.y - VIEW_HEIGHT // 2
        self.selected_tile = (self.player_unit.x, self.player_unit.y)

        self.notification_text = None  # 当前提示文本
        self.notification_timer = 0  # 提示文本的计时器
        self.stats_panel_timer = 0  # 数值面板计时器（以帧计时）
        self.stats_panel_timer = FPS * 3  # 游戏开始时显示面板 3 秒
        self.smoke_effect = None  # 当前烟雾效果

    def generate_weapons(self, num_weapons):
        """随机生成指定数量的武器并放置在地图上。"""
        for _ in range(num_weapons):
            while True:
                x = random.randint(0, GRID_WIDTH - 1)
                y = random.randint(0, GRID_HEIGHT - 1)
                if not self.environment.is_obstacle(x, y):  # 确保武器不生成在障碍物上
                    self.weapons.append(Weapon(x, y))
                    break

    def generate_health_potions(self, num_potions):
        """随机生成指定数量的药水"""
        for _ in range(num_potions):
            while True:
                x = random.randint(0, GRID_WIDTH - 1)
                y = random.randint(0, GRID_HEIGHT - 1)
                # 确保药水不出现在障碍物或武器的位置上
                if not self.environment.is_obstacle(x, y) and all(
                    weapon.x != x or weapon.y != y for weapon in self.weapons
                ):
                    self.health_potions.append(HealthPotion(x, y))
                    break

    def draw_stats_panel(self):
        """绘制数值面板，显示角色的当前数值"""
        if self.stats_panel_timer > 0:  # 如果计时器大于 0，显示面板
            panel_width = 150
            panel_height = 100

            # 动态计算面板位置（人物的屏幕坐标右侧）
            player_screen_x = (self.player_unit.x - self.camera_x) * CELL_SIZE
            player_screen_y = (self.player_unit.y - self.camera_y) * CELL_SIZE
            panel_x = player_screen_x + CELL_SIZE + 10  # 人物右侧
            panel_y = player_screen_y

            # 确保面板不会超出屏幕边界
            if panel_x + panel_width > SCREEN_WIDTH:
                panel_x = player_screen_x - panel_width - 10  # 改为左侧
            if panel_y + panel_height > SCREEN_HEIGHT:
                panel_y = SCREEN_HEIGHT - panel_height - 10  # 向上调整

            # 绘制面板背景
            pygame.draw.rect(self.screen, (0, 0, 0), (panel_x, panel_y, panel_width, panel_height))
            pygame.draw.rect(self.screen, (255, 255, 255), (panel_x, panel_y, panel_width, panel_height), 2)

            # 显示数值信息
            font = pygame.font.Font(None, 24)
            text_lines = [
                f"Health: {self.player_unit.health}",
                f"Attack: {self.player_unit.attack_power}",
                f"Speed: {self.player_unit.speed}",
                f"Env: {self.player_unit.environment}",
            ]
            for i, line in enumerate(text_lines):
                text_surface = font.render(line, True, (255, 255, 255))
                self.screen.blit(text_surface, (panel_x + 10, panel_y + 10 + i * 20))

            # 递减计时器
            self.stats_panel_timer -= 1

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
                # 检查拾取武器
                for weapon in self.weapons:
                    if weapon.x == self.player_unit.x and weapon.y == self.player_unit.y:
                        self.player_unit.pick_up_weapon(weapon)
                        self.weapons.remove(weapon)  # 移除拾取的武器
                        self.notification_timer = FPS * 2
                        self.stats_panel_timer = FPS * 3  # 显示数值面板
                        break  # 找到后跳出循环

                # 检查拾取药水
                for potion in self.health_potions:
                    if potion.x == self.player_unit.x and potion.y == self.player_unit.y:
                        self.player_unit.health = min(100, self.player_unit.health + potion.health_boost)
                        self.health_potions.remove(potion)
                        self.notification_text = "Health +20!"
                        self.notification_timer = FPS * 2
                        self.stats_panel_timer = FPS * 3  # 显示数值面板
                        break

                self.selected_tile = (self.player_unit.x, self.player_unit.y)

        # 触发烟雾技能
        if keys[pygame.K_SPACE] and not self.smoke_effect:  # 如果没有烟雾效果，且按下空格键
            self.smoke_effect = Smoke(self.player_unit.x, self.player_unit.y, duration=FPS * 10)  # 持续10秒

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

    def is_in_smoke(self, x, y):
        """检查给定坐标是否在烟雾范围内"""
        if self.smoke_effect:
            smoke_start_x = self.smoke_effect.x - self.smoke_effect.size // 2
            smoke_start_y = self.smoke_effect.y - self.smoke_effect.size // 2
            smoke_end_x = smoke_start_x + self.smoke_effect.size
            smoke_end_y = smoke_start_y + self.smoke_effect.size
            return smoke_start_x <= x < smoke_end_x and smoke_start_y <= y < smoke_end_y
        return False
    
    def draw(self):
        self.screen.fill((0, 0, 0))
        self.environment.draw_with_camera(self.screen, CELL_SIZE, self.camera_x, self.camera_y, VIEW_WIDTH, VIEW_HEIGHT)

        # Dessiner les cases accessibles
        self.draw_accessible_tiles()

        # 绘制烟雾
        if self.smoke_effect:
            self.smoke_effect.draw(self.screen, self.camera_x, self.camera_y, CELL_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT)

        # 绘制所有武器
        for weapon in self.weapons:
            weapon_screen_x = (weapon.x - self.camera_x) * CELL_SIZE
            weapon_screen_y = (weapon.y - self.camera_y) * CELL_SIZE
            weapon.draw(self.screen, weapon_screen_x, weapon_screen_y)

        # 绘制所有药水
        for potion in self.health_potions:
            potion_screen_x = (potion.x - self.camera_x) * CELL_SIZE
            potion_screen_y = (potion.y - self.camera_y) * CELL_SIZE
            potion.draw(self.screen, potion_screen_x, potion_screen_y)

        # Dessiner l'unité
        player_screen_x = (self.player_unit.x - self.camera_x) * CELL_SIZE
        player_screen_y = (self.player_unit.y - self.camera_y) * CELL_SIZE
        # 检查烟雾效果是否覆盖角色
        if not self.is_in_smoke(self.player_unit.x, self.player_unit.y):
            self.player_unit.draw(self.screen, player_screen_x, player_screen_y)

        # 绘制提示文本
        if self.notification_text and self.notification_timer > 0:
            font = pygame.font.Font(None, 36)
            text_surface = font.render(self.notification_text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))  # 屏幕顶部居中
            self.screen.blit(text_surface, text_rect)
            self.notification_timer -= 1  # 计时器递减
            
        if self.notification_timer == 0:
            self.notification_text = None  # 清除文本

        # 绘制数值面板
        self.draw_stats_panel()


        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:  
                    if event.key == pygame.K_ESCAPE: 
                        running = False  
            # 更新烟雾持续时间
            if self.smoke_effect:
                self.smoke_effect.duration -= 1
                if self.smoke_effect.duration <= 0:
                    self.smoke_effect = None  # 移除烟雾效果

            self.handle_input()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
>>>>>>> 3331b19fd10f7070c112e7aff66bcf3771779d84
