import os
import threading
import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import main  # Assuming your main server script is named main.py

class TestGameUI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.server_thread = threading.Thread(target=main.run_server, daemon=True)
        cls.server_thread.start()
        time.sleep(1)  # Give the server a moment to start

        options = Options()
        options.add_argument("--headless")
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

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()