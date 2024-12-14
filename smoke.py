import pygame


class Smoke:
    def __init__(self, x, y, duration, size=9):
        self.x = x
        self.y = y
        self.duration = duration  # 持续时间（帧数）
        self.size = size  # 烟雾覆盖范围（格子大小）
        self.image = pygame.image.load("smoke.png").convert_alpha()  # 烟雾的图片

    def draw(self, screen, camera_x, camera_y, cell_size, screen_width, screen_height):
        """绘制烟雾到屏幕上"""
        smoke_start_x = self.x - self.size // 2
        smoke_start_y = self.y - self.size // 2

        for dy in range(self.size):
            for dx in range(self.size):
                screen_x = (smoke_start_x + dx - camera_x) * cell_size
                screen_y = (smoke_start_y + dy - camera_y) * cell_size
                if 0 <= screen_x < screen_width and 0 <= screen_y < screen_height:
                    screen.blit(pygame.transform.scale(self.image, (cell_size, cell_size)), (screen_x, screen_y))