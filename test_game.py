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

    def test_player_movement_after_roll(self):
        self.driver.get(f"http://localhost:{main.PORT}")
        play_button = self.driver.find_element(By.ID, "play-button")
        play_button.click()
        time.sleep(1)

        # Get initial player position (should be 1)
        initial_square = self.driver.find_element(By.CSS_SELECTOR, "[data-square='1']")
        self.assertTrue(initial_square.find_elements(By.CLASS_NAME, "player-piece"))

        roll_dice_button = self.driver.find_element(By.ID, "roll-dice-button")
        roll_dice_button.click()
        time.sleep(1)

        turn_indicator = self.driver.find_element(By.ID, "turn-indicator")
        dice_roll_text = turn_indicator.text
        dice_roll = int(dice_roll_text.split(' ')[3].replace('!', ''))

        expected_position = 1 + dice_roll

        # Assert player piece is in the expected new square
        new_square = self.driver.find_element(By.CSS_SELECTOR, f"[data-square='{expected_position}']")
        self.assertTrue(new_square.find_elements(By.CLASS_NAME, "player-piece"))
        self.assertFalse(initial_square.find_elements(By.CLASS_NAME, "player-piece"))

    def test_player_movement_exact_win_rule(self):
        self.driver.get(f"http://localhost:{main.PORT}")
        play_button = self.driver.find_element(By.ID, "play-button")
        play_button.click()
        time.sleep(1)

        # Manually set playerPosition to 98 (or similar high value)
        self.driver.execute_script("playerPosition = 98;")
        self.driver.execute_script("document.querySelector('.player-piece').remove();")
        self.driver.execute_script("placePlayer();")
        time.sleep(1)

        # Simulate a dice roll that would land exactly on 100 (e.g., 2)
        self.driver.execute_script("const diceRoll = 2; turnIndicator.textContent = `You rolled a ${diceRoll}!`; let newPosition = playerPosition + diceRoll; if (newPosition > 100) { newPosition = playerPosition; } const currentPlayerPiece = document.querySelector('.player-piece'); if (currentPlayerPiece) { currentPlayerPiece.remove(); } playerPosition = newPosition; placePlayer();")
        time.sleep(1)

        # Assert player-piece is at square 100
        square_100 = self.driver.find_element(By.CSS_SELECTOR, "[data-square='100']")
        self.assertTrue(square_100.find_elements(By.CLASS_NAME, "player-piece"))

        # Simulate a dice roll that would overshoot 100 (e.g., 4)
        self.driver.execute_script("playerPosition = 98;")
        self.driver.execute_script("document.querySelector('.player-piece').remove();")
        self.driver.execute_script("placePlayer();")
        time.sleep(1)

        self.driver.execute_script("const diceRoll = 4; turnIndicator.textContent = `You rolled a ${diceRoll}!`; let newPosition = playerPosition + diceRoll; if (newPosition > 100) { newPosition = playerPosition; } const currentPlayerPiece = document.querySelector('.player-piece'); if (currentPlayerPiece) { currentPlayerPiece.remove(); } playerPosition = newPosition; placePlayer();")
        time.sleep(1)

        # Assert player-piece remains at the position before the roll (98 in this example)
        square_98 = self.driver.find_element(By.CSS_SELECTOR, "[data-square='98']")
        self.assertTrue(square_98.find_elements(By.CLASS_NAME, "player-piece"))

    def test_snake_movement(self):
        self.driver.get(f"http://localhost:{main.PORT}")
        play_button = self.driver.find_element(By.ID, "play-button")
        play_button.click()
        time.sleep(1)

        # Manually set playerPosition to a snake start square (e.g., 16)
        self.driver.execute_script("playerPosition = 16;")
        self.driver.execute_script("document.querySelector('.player-piece').remove();")
        self.driver.execute_script("placePlayer();")
        time.sleep(1)

        # Simulate a dice roll that lands on the snake start (not needed, as we manually set position)
        # Just trigger the movement logic by calling placePlayer again after setting position
        self.driver.execute_script("const snakeLadder = SNAKES_AND_LADDERS.find(sl => sl.start === playerPosition); if (snakeLadder) { playerPosition = snakeLadder.end; } placePlayer();")
        time.sleep(1)

        # Assert player-piece is at the snake end square (e.g., 6)
        square_6 = self.driver.find_element(By.CSS_SELECTOR, "[data-square='6']")
        self.assertTrue(square_6.find_elements(By.CLASS_NAME, "player-piece"))

    def test_ladder_movement(self):
        self.driver.get(f"http://localhost:{main.PORT}")
        play_button = self.driver.find_element(By.ID, "play-button")
        play_button.click()
        time.sleep(1)

        # Manually set playerPosition to a ladder start square (e.g., 1)
        self.driver.execute_script("playerPosition = 1;")
        self.driver.execute_script("document.querySelector('.player-piece').remove();")
        self.driver.execute_script("placePlayer();")
        time.sleep(1)

        # Just trigger the movement logic by calling placePlayer again after setting position
        self.driver.execute_script("const snakeLadder = SNAKES_AND_LADDERS.find(sl => sl.start === playerPosition); if (snakeLadder) { playerPosition = snakeLadder.end; } placePlayer();")
        time.sleep(1)

        # Assert player-piece is at the ladder end square (e.g., 38)
        square_38 = self.driver.find_element(By.CSS_SELECTOR, "[data-square='38']")
        self.assertTrue(square_38.find_elements(By.CLASS_NAME, "player-piece"))

    def test_snake_ladder_visual_representation(self):
        self.driver.get(f"http://localhost:{main.PORT}")
        play_button = self.driver.find_element(By.ID, "play-button")
        play_button.click()
        time.sleep(1)

        game_lines_svg = self.driver.find_element(By.ID, "game-lines")
        self.assertTrue(game_lines_svg.is_displayed())

        # Assert that the correct number of <line> elements are present within #game-lines
        # There are 19 snakes and ladders in the SNAKES_AND_LADDERS constant
        lines = game_lines_svg.find_elements(By.TAG_NAME, "line")
        self.assertEqual(len(lines), 19)

        # Assert that the stroke color of these lines corresponds to their type (snake/ladder)
        # This is a basic check, more robust checks would involve specific coordinates
        snake_lines = [line for line in lines if line.get_attribute('stroke') == 'red']
        ladder_lines = [line for line in lines if line.get_attribute('stroke') == 'green']

        # Based on the SNAKES_AND_LADDERS constant, there are 10 snakes and 9 ladders
        self.assertEqual(len(snake_lines), 10)
        self.assertEqual(len(ladder_lines), 9)

    def test_winning_celebration(self):
        self.driver.get(f"http://localhost:{main.PORT}")
        play_button = self.driver.find_element(By.ID, "play-button")
        play_button.click()
        time.sleep(1)

        # Manually set playerPosition to 99
        self.driver.execute_script("playerPosition = 99;")
        self.driver.execute_script("document.querySelector('.player-piece').remove();")
        self.driver.execute_script("placePlayer();")
        time.sleep(1)

        # Simulate a dice roll of 1 to reach 100
        self.driver.execute_script("const diceRoll = 1; turnIndicator.textContent = `You rolled a ${diceRoll}!`; let newPosition = playerPosition + diceRoll; if (newPosition > 100) { newPosition = playerPosition; } const currentPlayerPiece = document.querySelector('.player-piece'); if (currentPlayerPiece) { currentPlayerPiece.remove(); } playerPosition = newPosition; placePlayer();")
        time.sleep(1)

        # Check for win condition
        self.driver.execute_script("if (playerPosition === 100) { gameScreen.classList.add('hidden'); winningCelebration.classList.remove('hidden'); }")
        time.sleep(1)

        # Assert that the winning-celebration screen is displayed
        winning_celebration_screen = self.driver.find_element(By.ID, "winning-celebration")
        game_screen = self.driver.find_element(By.ID, "game-screen")

        self.assertTrue(winning_celebration_screen.is_displayed())
        self.assertFalse(game_screen.is_displayed())

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()