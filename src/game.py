import pygame
import sys

class PingPongGame:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Ping Pong Game")
        self.clock = pygame.time.Clock()

        self.paddle = pygame.Rect(self.WIDTH // 2 - 70, self.HEIGHT - 30, 140, 20)
        self.ball = pygame.Rect(self.WIDTH // 2 - 15, self.HEIGHT // 2 - 15, 30, 30)
        self.ball_speed_x = 7 * (-1 if pygame.time.get_ticks() % 2 else 1)
        self.ball_speed_y = 7

        self.bg_color = (0, 0, 0)
        self.paddle_color = (200, 200, 200)
        self.ball_color = (200, 200, 200)
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 36)

        # Load sounds
        self.ball_hit_sound = pygame.mixer.Sound("../assets/sounds/ball_hit.wav")

        self.score = 0
        self.pause = False
        self.game_over = False
        self.show_start_screen = True

    def handle_gesture(self, gesture):
        if gesture == "pause":
            self.pause = not self.pause

    def reset(self):
        self.__init__()

    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect()
        textrect.center = (x, y)
        surface.blit(textobj, textrect)

    def run(self, paddle_x):
        if self.show_start_screen:
            self.screen.fill(self.bg_color)
            self.draw_text('GAME START', self.font, (255, 255, 255), self.screen, self.WIDTH // 2, self.HEIGHT // 2)
            self.draw_text('Click to Start', self.small_font, (255, 255, 255), self.screen, self.WIDTH // 2, self.HEIGHT // 2 + 50)
            pygame.display.flip()
            return

        if self.game_over:
            self.screen.fill(self.bg_color)
            self.draw_text('GAME OVER', self.font, (255, 255, 255), self.screen, self.WIDTH // 2, self.HEIGHT // 2)
            self.draw_text('Click to Replay', self.small_font, (255, 255, 255), self.screen, self.WIDTH // 2, self.HEIGHT // 2 + 50)
            pygame.display.flip()
            return

        if self.pause:
            return

        self.paddle.x = max(0, min(paddle_x - self.paddle.width // 2, self.WIDTH - self.paddle.width))

        self.screen.fill(self.bg_color)

        self.ball.x += self.ball_speed_x
        self.ball.y += self.ball_speed_y

        if self.ball.top <= 0:
            self.ball_speed_y *= -1
            self.ball_hit_sound.play()
        if self.ball.left <= 0 or self.ball.right >= self.WIDTH:
            self.ball_speed_x *= -1
            self.ball_hit_sound.play()
        if self.ball.colliderect(self.paddle):
            self.ball_speed_y *= -1
            self.ball_hit_sound.play()
            self.score += 1

        if self.ball.bottom >= self.HEIGHT:
            self.game_over = True

        pygame.draw.rect(self.screen, self.paddle_color, self.paddle)
        pygame.draw.ellipse(self.screen, self.ball_color, self.ball)

        # Display the score
        score_text = self.font.render(str(self.score), True, (255, 255, 255))
        self.screen.blit(score_text, (self.WIDTH // 2 - score_text.get_width() // 2, 10))

        pygame.display.flip()
        self.clock.tick(60)
