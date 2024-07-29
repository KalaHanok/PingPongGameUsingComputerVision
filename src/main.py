import cv2
import pygame
from hand_tracking import HandTracker
from game import PingPongGame
from settings import SettingsMenu
from menu import MainMenu

def main():
    pygame.init()
    hand_tracker = HandTracker()
    game = PingPongGame()
    settings_menu = SettingsMenu()
    main_menu = MainMenu()
    cap = cv2.VideoCapture(0)
    state = "menu"

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        hand_x, gesture, annotated_image = hand_tracker.get_hand_position(frame)
        print(gesture)

        if state == "menu":
            action = main_menu.handle_gesture(gesture)
            if action == 0:  # Start Game
                game.show_start_screen = False
                state = "game"
            elif action == 1:  # Settings
                state = "settings"
            main_menu.draw(game.screen)

        elif state == "game":
            if game.show_start_screen:
                game.run(hand_x or game.WIDTH // 2)
                if gesture == "click":
                    game.show_start_screen = False
            elif game.game_over:
                game.run(hand_x or game.WIDTH // 2)
                if gesture == "click":
                    game.reset()
                    state = "menu"
            else:
                game.handle_gesture(gesture)
                game.run(hand_x or game.WIDTH // 2)

        elif state == "settings":
            new_state = settings_menu.handle_gesture(gesture)
            if new_state == "menu":
                state = "menu"
            settings_menu.draw(game.screen)

        cv2.imshow('Hand Tracking', annotated_image)
        if cv2.waitKey(5) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
