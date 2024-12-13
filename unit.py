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

    def attack(self, target):
        """Basic attack on another unit."""
        if target:
            print(f"{self.unit_type} attacks {target.unit_type} for {self.attack_power} damage!")
            target.health -= self.attack_power
            if target.health <= 0:
                print(f"{target.unit_type} has been defeated!")

    def has_enough_skill_points(self, cost):
        """Checks if the unit has enough skill points to use a skill."""
        return self.skill_points >= cost

    def use_skill(self, skill_number):
        """Uses a skill based on the skill number."""
        if skill_number == 1:
            return self.skill_one()
        elif skill_number == 2:
            return self.skill_two()
        elif skill_number == 3:
            return self.skill_three()
        return False

    def skill_one(self):
        """Override this method for specific skill 1."""
        print(f"{self.unit_type} does not have Skill 1.")
        return False

    def skill_two(self):
        """Override this method for specific skill 2."""
        print(f"{self.unit_type} does not have Skill 2.")
        return False

    def skill_three(self):
        """Override this method for specific skill 3."""
        print(f"{self.unit_type} does not have Skill 3.")
        return False

    def update_skill_points(self):
        """Increases skill points at the end of a turn."""
        if self.skill_points < self.max_skill_points:
            self.skill_points += 1

class Human(Unit):
    """Human unit."""
    def __init__(self, x, y):
        super().__init__(x, y, health=100, attack_power=15, speed=3, environment="plain")
        self.unit_type = "Human"
        self.load_image("Human.png")

    def skill_one(self):
        cost = 3
        if self.has_enough_skill_points(cost):
            print(f"{self.unit_type} uses Charge!")
            self.skill_points -= cost
            return True
        return False

    def skill_two(self):
        cost = 3
        if self.has_enough_skill_points(cost):
            print(f"{self.unit_type} uses Shield Protection!")
            self.skill_points -= cost
            return True
        return False

    def skill_three(self):
        cost = 4
        if self.has_enough_skill_points(cost):
            print(f"{self.unit_type} uses Rally Cry!")
            self.skill_points -= cost
            return True
        return False

class Elf(Unit):
    """Elf unit."""
    def __init__(self, x, y):
        super().__init__(x, y, health=80, attack_power=20, speed=4, environment="forest")
        self.unit_type = "Elf"
        self.load_image("Elf.png")

    def skill_one(self):
        cost = 2
        if self.has_enough_skill_points(cost):
            print(f"{self.unit_type} uses Enchanted Arrow!")
            self.skill_points -= cost
            return True
        return False

    def skill_two(self):
        cost = 3
        if self.has_enough_skill_points(cost):
            print(f"{self.unit_type} uses Eagle Vision!")
            self.skill_points -= cost
            return True
        return False

    def skill_three(self):
        cost = 3
        if self.has_enough_skill_points(cost):
            print(f"{self.unit_type} uses Rapid Shot!")
            self.skill_points -= cost
            return True
        return False

class Orc(Unit):
    """Orc unit."""
    def __init__(self, x, y):
        super().__init__(x, y, health=90, attack_power=18, speed=3, environment="swamp")
        self.unit_type = "Orc"
        self.load_image("Orc.png")

    def skill_one(self):
        cost = 3
        if self.has_enough_skill_points(cost):
            print(f"{self.unit_type} uses War Cry!")
            self.skill_points -= cost
            return True
        return False

    def skill_two(self):
        cost = 4
        if self.has_enough_skill_points(cost):
            print(f"{self.unit_type} uses Berserk!")
            self.skill_points -= cost
            return True
        return False

    def skill_three(self):
        cost = 3
        if self.has_enough_skill_points(cost):
            print(f"{self.unit_type} uses Savage Leap!")
            self.skill_points -= cost
            return True
        return False

class Dwarf(Unit):
    """Dwarf unit."""
    def __init__(self, x, y):
        super().__init__(x, y, health=120, attack_power=10, speed=2, environment="mountain")
        self.unit_type = "Dwarf"
        self.load_image("Dwarf.png")

    def skill_one(self):
        cost = 3
        if self.has_enough_skill_points(cost):
            print(f"{self.unit_type} uses Mountain Fury!")
            self.skill_points -= cost
            self.health += 10  # Bonus temporary health
            return True
        return False

    def skill_two(self):
        cost = 4
        if self.has_enough_skill_points(cost):
            print(f"{self.unit_type} uses Hammer Slam!")
            self.skill_points -= cost
            return True
        return False

    def skill_three(self):
        cost = 3
        if self.has_enough_skill_points(cost):
            print(f"{self.unit_type} uses Stone Resilience!")
            self.skill_points -= cost
            self.health += 25
            return True
        return False

class Goblin(Unit):
    """Goblin unit."""
    def __init__(self, x, y):
        super().__init__(x, y, health=60, attack_power=12, speed=4, environment="obstacle")
        self.unit_type = "Goblin"
        self.load_image("Goblin.png")

    def skill_one(self):
        cost = 4
        if self.has_enough_skill_points(cost):
            print(f"{self.unit_type} uses Vanish!")
            self.skill_points -= cost
            return True
        return False

    def skill_two(self):
        cost = 3
        if self.has_enough_skill_points(cost):
            print(f"{self.unit_type} uses Explosive Trap!")
            self.skill_points -= cost
            return True
        return False

    def skill_three(self):
        cost = 2
        if self.has_enough_skill_points(cost):
            print(f"{self.unit_type} uses Backstab!")
            self.skill_points -= cost
            return True
        return False

class Troll(Unit):
    """Troll unit."""
    def __init__(self, x, y):
        super().__init__(x, y, health=200, attack_power=25, speed=2, environment="mixed")
        self.unit_type = "Troll"
        self.load_image("Troll.png")

    def skill_one(self):
        cost = 4
        if self.has_enough_skill_points(cost):
            print(f"{self.unit_type} uses Rapid Regeneration!")
            self.skill_points -= cost
            self.health += self.health * 0.3  # Recover 30% health
            return True
        return False

    def skill_two(self):
        cost = 5
        if self.has_enough_skill_points(cost):
            print(f"{self.unit_type} uses Crushing Blow!")
            self.skill_points -= cost
            return True
        return False

    def skill_three(self):
        cost = 3
        if self.has_enough_skill_points(cost):
            print(f"{self.unit_type} uses Terrifying Roar!")
            self.skill_points -= cost
            return True
        return False
