import pygame
from utils import draw_text, handle_gesture

class MainMenu:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 800, 600
        self.bg_color = (0, 0, 0)
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 36)

        self.menu_options = ["Start Game", "Settings"]
        self.current_selection = 0

    def draw(self, screen):
        screen.fill(self.bg_color)
        for idx, option in enumerate(self.menu_options):
            color = (255, 255, 255) if idx == self.current_selection else (100, 100, 100)
            draw_text(option, self.font, color, screen, self.WIDTH // 2, self.HEIGHT // 2 + idx * 100)
        pygame.display.flip()

    def handle_gesture(self, gesture):
        self.current_selection, action = handle_gesture(gesture, self.menu_options, self.current_selection)
        return action
