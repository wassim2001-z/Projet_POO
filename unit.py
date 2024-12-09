import pygame

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
        self.skill_points = 2
        self.max_skill_points = 11

    def load_image(self, image_path):
        """Loads an image for the unit using pygame."""
        try:
            self.image = pygame.image.load(image_path).convert_alpha()
        except pygame.error as e:
            print(f"Error loading image {image_path}: {e}")

    def draw(self, screen, screen_x=None, screen_y=None):
        """Draws the unit on the screen with a health bar and skill points."""
        if self.image:
            scaled_image = pygame.transform.scale(self.image, (60, 60))
            if screen_x is not None and screen_y is not None:
                screen.blit(scaled_image, (screen_x, screen_y))
            else:
                screen.blit(scaled_image, (self.x * 60, self.y * 60))

        # Draw health bar
        health_bar_width = 60
        health_ratio = self.health / 100  # Assuming max health is 100 for simplicity
        health_bar_height = 5
        pygame.draw.rect(screen, (255, 0, 0), (screen_x or self.x * 60, (screen_y or self.y * 60) - health_bar_height, health_bar_width, health_bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (screen_x or self.x * 60, (screen_y or self.y * 60) - health_bar_height, int(health_bar_width * health_ratio), health_bar_height))

        # Draw skill points
        font = pygame.font.Font(None, 20)
        skill_text = font.render(str(self.skill_points), True, (255, 255, 255))
        screen.blit(skill_text, ((screen_x or self.x * 60) + 5, (screen_y or self.y * 60) + 40))

    def has_enough_skill_points(self, cost):
        """Checks if the unit has enough skill points to use a skill."""
        return self.skill_points >= cost

    def update_skill_points(self):
        """Increases skill points at the end of a turn."""
        if self.skill_points < self.max_skill_points:
            self.skill_points += 0.5

class Human(Unit):
    """Human unit."""
    def __init__(self, x, y):
        super().__init__(x, y, health=100, attack_power=15, speed=3, environment="plain")
        self.unit_type = "Human"
        self.load_image("Human.png")

    def charge(self, target):
        cost = 3
        if self.has_enough_skill_points(cost):
            self.skill_points -= cost
            target.health -= self.attack_power * 1.5  # 150% attack damage

    def shield_protection(self):
        cost = 3
        if self.has_enough_skill_points(cost):
            self.skill_points -= cost

    def rally_cry(self, allies):
        cost = 4
        if self.has_enough_skill_points(cost):
            self.skill_points -= cost
            for ally in allies:
                ally.attack_power += ally.attack_power * 0.2  # Increase attack by 20%

class Elf(Unit):
    """Elf unit."""
    def __init__(self, x, y):
        super().__init__(x, y, health=80, attack_power=20, speed=4, environment="forest")
        self.unit_type = "Elf"
        self.load_image("Elf.png")

    def enchanted_arrow(self, targets):
        cost = 2
        if self.has_enough_skill_points(cost):
            self.skill_points -= cost
            for target in targets:
                target.health -= self.attack_power * 1.2  # 120% attack damage

    def eagle_vision(self):
        cost = 3
        if self.has_enough_skill_points(cost):
            self.skill_points -= cost

    def rapid_shot(self, targets):
        cost = 3
        if self.has_enough_skill_points(cost):
            self.skill_points -= cost
            for target in targets[:2]:  # Up to two targets
                target.health -= self.attack_power

class Dwarf(Unit):
    """Dwarf unit."""
    def __init__(self, x, y):
        super().__init__(x, y, health=120, attack_power=10, speed=2, environment="mountain")
        self.unit_type = "Dwarf"
        self.load_image("Dwarf.png")

    def mountain_fury(self):
        cost = 3
        if self.has_enough_skill_points(cost):
            self.skill_points -= cost
            self.health += 10  # Temporary bonus health

    def hammer_slam(self, targets):
        cost = 4
        if self.has_enough_skill_points(cost):
            self.skill_points -= cost
            for target in targets:
                target.health -= self.attack_power

    def stone_resilience(self):
        cost = 3
        if self.has_enough_skill_points(cost):
            self.skill_points -= cost
            self.health += 25  # Recover health

class Orc(Unit):
    """Orc unit."""
    def __init__(self, x, y):
        super().__init__(x, y, health=90, attack_power=18, speed=3, environment="swamp")
        self.unit_type = "Orc"
        self.load_image("Orc.png")

    def war_cry(self, targets):
        cost = 3
        if self.has_enough_skill_points(cost):
            self.skill_points -= cost
            for target in targets:
                target.attack_power -= target.attack_power * 0.25  # Reduce attack power by 25%

    def berserk(self):
        cost = 4
        if self.has_enough_skill_points(cost):
            self.skill_points -= cost
            self.attack_power += self.attack_power * 0.5  # Increase attack by 50%
            self.health -= self.health * 0.2  # Reduce defense

    def savage_leap(self, target):
        cost = 3
        if self.has_enough_skill_points(cost):
            self.skill_points -= cost
            target.health -= self.attack_power  # Apply damage

class Goblin(Unit):
    """Goblin unit."""
    def __init__(self, x, y):
        super().__init__(x, y, health=60, attack_power=12, speed=4, environment="obstacle")
        self.unit_type = "Goblin"
        self.load_image("Goblin.png")

    def vanish(self):
        cost = 4
        if self.has_enough_skill_points(cost):
            self.skill_points -= cost

    def explosive_trap(self, target):
        cost = 3
        if self.has_enough_skill_points(cost):
            self.skill_points -= cost
            target.health -= 15  # Fixed damage

    def backstab(self, target):
        cost = 2
        if self.has_enough_skill_points(cost):
            self.skill_points -= cost
            target.health -= self.attack_power * 1.5

class Troll(Unit):
    """Troll unit."""
    def __init__(self, x, y):
        super().__init__(x, y, health=200, attack_power=25, speed=2, environment="mixed")
        self.unit_type = "Troll"
        self.load_image("Troll.png")

    def rapid_regeneration(self):
        cost = 4
        if self.has_enough_skill_points(cost):
            self.skill_points -= cost
            self.health += self.health * 0.3  # Recover 30% health

    def crushing_blow(self, targets):
        cost = 5
        if self.has_enough_skill_points(cost):
            self.skill_points -= cost
            for target in targets:
                target.health -= self.attack_power  # Heavy damage

    def terrifying_roar(self, targets):
        cost = 3
        if self.has_enough_skill_points(cost):
            self.skill_points -= cost
            for target in targets:
                target.attack_power -= target.attack_power * 0.2
