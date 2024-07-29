import unittest
from hand_tracking import HandTracker
from game import PingPongGame
from menu import MainMenu
from settings import SettingsMenu
import cv2

class TestHandTracker(unittest.TestCase):
    def setUp(self):
        self.hand_tracker = HandTracker()
        # Assuming you have test images for testing purposes
        self.test_image_with_hand = cv2.imread("test_hand_image.jpg")  # Path to a test image with a hand
        self.test_image_without_hand = cv2.imread("test_no_hand_image.jpg")  # Path to a test image without a hand

    def test_get_hand_position_success(self):
        hand_x, gesture, frame = self.hand_tracker.get_hand_position(self.test_image_with_hand)
        self.assertIsNotNone(hand_x)
        self.assertNotEqual(gesture, "Unknown")

    def test_get_hand_position_failure(self):
        hand_x, gesture, frame = self.hand_tracker.get_hand_position(self.test_image_without_hand)
        self.assertIsNone(hand_x)
        self.assertEqual(gesture, "Unknown")

class TestPingPongGame(unittest.TestCase):
    def setUp(self):
        self.game = PingPongGame()

    def test_game_start(self):
        self.game.start()
        self.assertTrue(self.game.is_running)

    def test_game_pause(self):
        self.game.start()
        self.game.pause()
        self.assertFalse(self.game.is_running)

class TestMainMenu(unittest.TestCase):
    def setUp(self):
        self.menu = MainMenu()

    def test_show_main_menu(self):
        self.menu.show_main_menu()
        self.assertTrue(self.menu.main_menu_displayed)

    def test_show_settings_menu(self):
        self.menu.show_settings_menu()
        self.assertTrue(self.menu.settings_menu_displayed)

class TestSettingsMenu(unittest.TestCase):
    def setUp(self):
        self.settings = SettingsMenu()

    def test_change_background_music(self):
        self.settings.change_background_music("song.mp3")
        self.assertEqual(self.settings.current_background_music, "song.mp3")

class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.hand_tracker = HandTracker()
        self.game = PingPongGame()
        self.menu = MainMenu()
        self.settings = SettingsMenu()
        self.test_image_with_hand = cv2.imread("test_hand_image.jpg")

    def test_hand_tracking_integration(self):
        hand_x, gesture, frame = self.hand_tracker.get_hand_position(self.test_image_with_hand)
        self.game.handle_gesture(gesture)
        self.assertIn(gesture, ["Pause", "Setting", "Pointing", "MouseMove", "MouseClick"])

    def test_menu_to_game_integration(self):
        self.menu.show_main_menu()
        self.menu.start_game()
        self.assertTrue(self.game.is_running)

    def test_settings_music_integration(self):
        self.settings.change_background_music("song.mp3")
        self.assertEqual(self.settings.current_background_music, "song.mp3")

if __name__ == "__main__":
    unittest.main()
