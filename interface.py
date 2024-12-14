import pygame

class Interface:
    """Class to manage the user interface, including messages and unit statistics."""

    def __init__(self, width):
        self.width = width
        self.messages = []
        self.max_messages = 15  # Increased to display more messages

         # Load icons for units
        self.unit_icons = {
             "Elf": pygame.image.load("Elf.png"),  # Replace with actual file paths
             "Human": pygame.image.load("Human.png"),
             "Orc": pygame.image.load("Orc.png"),
             "Dwarf": pygame.image.load("Dwarf.png"),
             "Goblin": pygame.image.load("Goblin.png"),
             "Troll": pygame.image.load("Orc.png"),
         }

    def add_message(self, message_type, unit_type=None, skill_name=None, value=None):
        """Adds a new message to the interface based on the action type."""
        if message_type == "attack":
            message = f"{unit_type} attacked for {value} damage!"
        elif message_type == "skill":
            message = f"{unit_type} used the skill: {skill_name}!"
        else:
            return  # Skip adding irrelevant messages like movement

        self.messages.insert(0, message)  # New messages appear at the top
        if len(self.messages) > self.max_messages:
            self.messages.pop()

    def draw(self, screen, units):
        """Draws the interface including messages and unit statistics."""
        sidebar_x = screen.get_width() - self.width

        # Draw sidebar background with a gradient effect
        for y in range(screen.get_height()):
            color = (50 + y // 10, 50 + y // 15, 50 + y // 20)  # Gradient effect
            pygame.draw.line(screen, color, (sidebar_x, y), (sidebar_x + self.width, y))

        # Draw a title at the top
        font_title = pygame.font.Font(None, 36)
        title_surface = font_title.render("Game Interface", True, (255, 255, 255))
        screen.blit(title_surface, (sidebar_x + 10, 10))

        # Draw a separator below the title
        pygame.draw.line(screen, (200, 200, 200), (sidebar_x, 50), (sidebar_x + self.width, 50), 2)

        # Draw unit icons and stats at the top
        y_offset = 60
        for unit in units:
            # Draw unit icon
            if unit.unit_type in self.unit_icons:
                unit_icon = pygame.transform.scale(self.unit_icons[unit.unit_type], (40, 40))  # Larger icons
                screen.blit(unit_icon, (sidebar_x + 10, y_offset))

            # Draw health bar
            pygame.draw.rect(screen, (255, 0, 0), (sidebar_x + 60, y_offset + 10, 150, 15))  # Red bar
            pygame.draw.rect(screen, (0, 255, 0), (sidebar_x + 60, y_offset + 10, int(150 * (unit.health / 100)), 15))  # Green bar

            # Draw skill points bar below health
            pygame.draw.rect(screen, (50, 50, 255), (sidebar_x + 60, y_offset + 30, 150, 15))  # Blue bar
            pygame.draw.rect(screen, (0, 255, 255), (sidebar_x + 60, y_offset + 30, int(150 * (unit.skill_points / unit.max_skill_points)), 15))  # Cyan bar

            y_offset += 60

        # Divider between unit stats and messages
        pygame.draw.line(screen, (200, 200, 200), (sidebar_x, y_offset), (sidebar_x + self.width, y_offset), 2)
        y_offset += 10

        # Draw messages
        font = pygame.font.Font(None, 24)
        for message in self.messages:
            text_surface = font.render(message, True, (255, 255, 255))
            screen.blit(text_surface, (sidebar_x + 10, y_offset))
            y_offset += 30

        # Final border for aesthetics
        pygame.draw.rect(screen, (255, 255, 255), (sidebar_x, 0, self.width, screen.get_height()), 2)

    def reset_messages(self):
        """Clears all messages from the interface."""
        self.messages = []
