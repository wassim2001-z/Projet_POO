import pygame


class Smoke:
    def __init__(self, x, y, size=7, duration=300):
        self.x = x
        self.y = y
        self.size = size
        self.duration = duration  # 持续时间，单位是帧数
        self.image = pygame.image.load("smoke.png").convert_alpha()  # 自定义烟雾图片

    def draw(self, screen, camera_x, camera_y, cell_size):
        """绘制烟雾区域"""
        start_x = self.x - self.size // 2
        start_y = self.y - self.size // 2
        for dy in range(self.size):
            for dx in range(self.size):
                tile_x = start_x + dx
                tile_y = start_y + dy
                screen_x = (tile_x - camera_x) * cell_size
                screen_y = (tile_y - camera_y) * cell_size
                screen.blit(pygame.transform.scale(self.image, (cell_size, cell_size)), (screen_x, screen_y))

    def is_in_smoke(self, unit_x, unit_y):
        """检查单位是否处于烟雾区域内"""
        start_x = self.x - self.size // 2
        start_y = self.y - self.size // 2
        return start_x <= unit_x < start_x + self.size and start_y <= unit_y < start_y + self.size