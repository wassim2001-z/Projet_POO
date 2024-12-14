import pygame

class Venom:
    def __init__(self, x, y, size=5):
        self.x = x  # 中心位置 x 坐标
        self.y = y  # 中心位置 y 坐标
        self.size = size  # 区域大小（正方形边长）
        self.image = pygame.image.load("venom.png").convert_alpha()  # 毒液图片

    def draw(self, screen, camera_x, camera_y, cell_size):
        """绘制毒液区域"""
        start_x = self.x - self.size // 2
        start_y = self.y - self.size // 2
        for dy in range(self.size):
            for dx in range(self.size):
                tile_x = start_x + dx
                tile_y = start_y + dy
                screen_x = (tile_x - camera_x) * cell_size
                screen_y = (tile_y - camera_y) * cell_size
                screen.blit(pygame.transform.scale(self.image, (cell_size, cell_size)), (screen_x, screen_y))

    def is_in_venom(self, unit_x, unit_y):
        """检查单位是否处于毒液区域内"""
        start_x = self.x - self.size // 2
        start_y = self.y - self.size // 2
        return start_x <= unit_x < start_x + self.size and start_y <= unit_y < start_y + self.size