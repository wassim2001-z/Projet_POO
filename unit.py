<<<<<<< HEAD
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
        self.weapon = None

    def pick_up_weapon(self, weapon):
        """Pick up a weapon and increase attack power."""
        if weapon and weapon.x == self.x and weapon.y == self.y:
            self.attack_power += weapon.attack_boost
            self.weapon = weapon

    def load_image(self, image_path):
        """Loads an image for the unit using pygame."""
        try:
            self.image = pygame.image.load(image_path).convert_alpha()
        except pygame.error as e:
            print(f"Error loading image {image_path}: {e}")

    def attack(self, target):
        """Default attack logic for units."""
        if target and target.health > 0:
            target.health -= self.attack_power
            print(f"{self.unit_type} attacked {target.unit_type} for {self.attack_power} damage!")
            if target.health <= 0:
                print(f"{target.unit_type} has been defeated!")

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

    def use_skill(self, skill_number):
        """Uses a skill based on the skill number."""
        if skill_number == 1:
            return self.skill_one()
        elif skill_number == 2:
            return self.skill_two()
        elif skill_number == 3:
            return self.skill_three()
        return None

    def skill_one(self):
        """Override this method for specific skill 1."""
        print(f"{self.unit_type} does not have Skill 1.")
        return None

    def skill_two(self):
        """Override this method for specific skill 2."""
        print(f"{self.unit_type} does not have Skill 2.")
        return None

    def skill_three(self):
        """Override this method for specific skill 3."""
        print(f"{self.unit_type} does not have Skill 3.")
        return None

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

    def skill_one(self):
        cost = 3
        if self.has_enough_skill_points(cost):
            self.skill_points -= cost
            return "Charge"
        return None

    def skill_two(self):
        cost = 3
        if self.has_enough_skill_points(cost):
            self.skill_points -= cost
            return "Shield Protection"
        return None

    def skill_three(self):
        cost = 4
        if self.has_enough_skill_points(cost):
            self.skill_points -= cost
            return "Rally Cry"
        return None

class Elf(Unit):
    """Elf unit."""
    def __init__(self, x, y):
        super().__init__(x, y, health=80, attack_power=20, speed=4, environment="forest")
        self.unit_type = "Elf"
        self.load_image("Elf.png")

    def skill_one(self):
        cost = 2
        if self.has_enough_skill_points(cost):
            self.skill_points -= cost
            return "Enchanted Arrow"
        return None

    def skill_two(self):
        cost = 3
        if self.has_enough_skill_points(cost):
            self.skill_points -= cost
            return "Eagle Vision"
        return None

    def skill_three(self):
        cost = 3
        if self.has_enough_skill_points(cost):
            self.skill_points -= cost
            return "Rapid Shot"
        return None

class Dwarf(Unit):
    """Dwarf unit."""
    def __init__(self, x, y):
        super().__init__(x, y, health=120, attack_power=10, speed=2, environment="mountain")
        self.unit_type = "Dwarf"
        self.load_image("Dwarf.png")
 
    def skill_one(self):
        cost = 3
        if self.has_enough_skill_points(cost):
            self.skill_points -= cost
            self.health += 10  # Temporary bonus health
            return "Mountain Fury"
        return None

    def skill_two(self):
        cost = 4
        if self.has_enough_skill_points(cost):
            self.skill_points -= cost
            return "Hammer Slam"
        return None

    def skill_three(self):
        cost = 3
        if self.has_enough_skill_points(cost):
            self.skill_points -= cost
            self.health += 25  # Recover health
            return "Stone Resilience"
        return None

class Orc(Unit):
    """Orc unit."""
    def __init__(self, x, y):
        super().__init__(x, y, health=90, attack_power=18, speed=3, environment="swamp")
        self.unit_type = "Orc"
        self.load_image("Orc.png")

    def skill_one(self):
        cost = 3
        if self.has_enough_skill_points(cost):
            self.skill_points -= cost
            return "War Cry"
        return None

    def skill_two(self):
        cost = 4
        if self.has_enough_skill_points(cost):
            self.skill_points -= cost
            self.attack_power += self.attack_power * 0.5  # Increase attack by 50%
            self.health -= self.health * 0.2  # Reduce defense
            return "Berserk"
        return None

    def skill_three(self):
        cost = 3
        if self.has_enough_skill_points(cost):
            self.skill_points -= cost
            return "Savage Leap"
        return None

class Goblin(Unit):
    """Goblin unit."""
    def __init__(self, x, y):
        super().__init__(x, y, health=60, attack_power=12, speed=4, environment="obstacle")
        self.unit_type = "Goblin"
        self.load_image("Goblin.png")

    def skill_one(self):
        cost = 4
        if self.has_enough_skill_points(cost):
            self.skill_points -= cost
            return "Vanish"
        return None

    def skill_two(self):
        cost = 3
        if self.has_enough_skill_points(cost):
            self.skill_points -= cost
            return "Explosive Trap"
        return None

    def skill_three(self):
        cost = 2
        if self.has_enough_skill_points(cost):
            self.skill_points -= cost
            return "Backstab"
        return None

class Troll(Unit):
    """Troll unit."""
    def __init__(self, x, y):
        super().__init__(x, y, health=200, attack_power=25, speed=2, environment="mixed")
        self.unit_type = "Troll"
        self.load_image("Troll.png")

    def skill_one(self):
        cost = 4
        if self.has_enough_skill_points(cost):
            self.skill_points -= cost
            self.health += self.health * 0.3  # Recover 30% health
            return "Rapid Regeneration"
        return None

    def skill_two(self):
        cost = 5
        if self.has_enough_skill_points(cost):
            self.skill_points -= cost
            return "Crushing Blow"
        return None

    def skill_three(self):
        cost = 3
        if self.has_enough_skill_points(cost):
            self.skill_points -= cost
            return "Terrifying Roar"
        return None

class Weapon:
    def __init__(self, x, y, attack_boost=5):
        self.x = x
        self.y = y
        self.attack_boost = attack_boost
        self.image = pygame.image.load("weapon.png").convert_alpha()

    def draw(self, screen, screen_x, screen_y):
        scaled_image = pygame.transform.scale(self.image, (60, 60))
        screen.blit(scaled_image, (screen_x, screen_y))

class HealthPotion:
    def __init__(self, x, y, health_boost=20):
        self.x = x
        self.y = y
        self.health_boost = health_boost
        self.image = pygame.image.load("health_potion.png").convert_alpha()

    def draw(self, screen, screen_x, screen_y):
        scaled_image = pygame.transform.scale(self.image, (60, 60))
        screen.blit(scaled_image, (screen_x, screen_y))
=======
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
        self.weapon = None

    def pick_up_weapon(self, weapon):
        """拾取武器并增加攻击力。"""
        if weapon and weapon.x == self.x and weapon.y == self.y:
            self.attack_power += weapon.attack_boost
            self.weapon = weapon  # 标记该单位已拾取武器
            
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

    def get_accessible_tiles(self, environment):
        """Calculates the tiles the unit can move to based on its speed and the environment."""
        accessible_tiles = []
        for dy in range(-self.speed, self.speed + 1):
            for dx in range(-self.speed, self.speed + 1):
                new_x, new_y = self.x + dx, self.y + dy
                if environment.is_within_bounds(new_x, new_y):
                    tile = environment.grid[new_y][new_x]
                    if tile and not tile.obstacle and tile.speed <= self.speed:
                        accessible_tiles.append((new_x, new_y))
        return accessible_tiles

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
class Weapon:
    def __init__(self, x, y, attack_boost=5):
        self.x = x
        self.y = y
        self.attack_boost = attack_boost
        self.image = pygame.image.load("weapon.png").convert_alpha()  # 假设武器图像为 `weapon.png`

    def draw(self, screen, screen_x, screen_y):
        scaled_image = pygame.transform.scale(self.image, (60, 60))
        screen.blit(scaled_image, (screen_x, screen_y))
        
class HealthPotion:
    def __init__(self, x, y, health_boost=20):
        self.x = x
        self.y = y
        self.health_boost = health_boost
        self.image = pygame.image.load("health_potion.png").convert_alpha()  # 假设药水图像为 `health_potion.png`

    def draw(self, screen, screen_x, screen_y):
        """绘制药水到屏幕上"""
        scaled_image = pygame.transform.scale(self.image, (60, 60))
        screen.blit(scaled_image, (screen_x, screen_y))
>>>>>>> 3331b19fd10f7070c112e7aff66bcf3771779d84
