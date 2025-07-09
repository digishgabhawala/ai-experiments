import os
import threading
import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import main  # Assuming your main server script is named main.py

class TestGameUI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.server_thread = threading.Thread(target=main.run_server, daemon=True)
        cls.server_thread.start()
        time.sleep(1)  # Give the server a moment to start

        options = Options()
        # options.add_argument("--headless")
        options.set_capability("goog:loggingPrefs", {"browser": "ALL"})
        cls.driver = webdriver.Chrome(options=options)

    def test_welcome_screen_and_transition(self):
        self.driver.get(f"http://localhost:{main.PORT}")

        welcome_screen = self.driver.find_element(By.ID, "welcome-screen")
        game_screen = self.driver.find_element(By.ID, "game-screen")

        self.assertTrue(welcome_screen.is_displayed())
        self.assertFalse(game_screen.is_displayed())

        play_button = self.driver.find_element(By.ID, "play-button")
        play_button.click()

        self.assertFalse(welcome_screen.is_displayed())
        self.assertTrue(game_screen.is_displayed())

    def test_game_board_creation(self):
        self.driver.get(f"http://localhost:{main.PORT}")
        play_button = self.driver.find_element(By.ID, "play-button")
        play_button.click()

        game_board = self.driver.find_element(By.ID, "game-board")
        squares = game_board.find_elements(By.CLASS_NAME, "square")

        self.assertEqual(len(squares), 100)
        self.assertEqual(squares[0].text, "1")
        self.assertEqual(squares[99].text, "100")

    def test_player_piece_initial_position(self):
        self.driver.get(f"http://localhost:{main.PORT}")
        play_button = self.driver.find_element(By.ID, "play-button")
        play_button.click()
        time.sleep(1)

        first_square = self.driver.find_element(By.CSS_SELECTOR, "[data-square='1']")
        player_piece = first_square.find_element(By.CLASS_NAME, "player-piece")
        self.assertTrue(player_piece.is_displayed())

    

    def test_turn_indicator_display(self):
        self.driver.get(f"http://localhost:{main.PORT}")
        play_button = self.driver.find_element(By.ID, "play-button")
        play_button.click()

        turn_indicator = self.driver.find_element(By.ID, "turn-indicator")
        self.assertTrue(turn_indicator.is_displayed())
        self.assertEqual(turn_indicator.text, "Your Turn")

    def test_dice_roll_display(self):
        self.driver.get(f"http://localhost:{main.PORT}")
        play_button = self.driver.find_element(By.ID, "play-button")
        play_button.click()
        time.sleep(1)

        roll_dice_button = self.driver.find_element(By.ID, "roll-dice-button")
        roll_dice_button.click()
        time.sleep(1)

        turn_indicator = self.driver.find_element(By.ID, "turn-indicator")
        self.assertTrue(turn_indicator.is_displayed())
        # Check if the text contains "You rolled a " and a number between 1 and 6
        self.assertRegex(turn_indicator.text, r"^You rolled a (1|2|3|4|5|6)!$")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()