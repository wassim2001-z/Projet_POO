import pygame
import random
from environment import Environment
from unit import Elf
from unit import Weapon
from unit import HealthPotion


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

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.environment.draw_with_camera(self.screen, CELL_SIZE, self.camera_x, self.camera_y, VIEW_WIDTH, VIEW_HEIGHT)

        # Dessiner les cases accessibles
        self.draw_accessible_tiles()

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

            self.handle_input()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
