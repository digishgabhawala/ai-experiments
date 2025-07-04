import unittest
import threading
import time
import os
import socketserver
import http.server
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException

# Assuming main.py is in the parent directory
from main import STATIC_DIR

# --- Test Server Setup ---

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass # Suppress logging

def run_server(server):
    server.serve_forever()

class TestStaticServer(unittest.TestCase):

    server = None
    server_thread = None
    driver = None
    test_url = None

    @classmethod
    def setUpClass(cls):
        """Set up a test server and a headless browser."""
        cls.original_cwd = os.getcwd()
        # The server needs to run from the static directory
        os.chdir(STATIC_DIR)

        # Find a free port
        s = socketserver.TCPServer(("", 0), QuietHandler)
        test_port = s.server_address[1]
        s.server_close()
        cls.test_url = f"http://localhost:{test_port}"

        # Start the server in a background thread
        cls.server = socketserver.TCPServer(("", test_port), QuietHandler)
        cls.server_thread = threading.Thread(target=run_server, args=(cls.server,))
        cls.server_thread.daemon = True
        cls.server_thread.start()
        time.sleep(1) # Give server a moment to start

        # Set up Selenium WebDriver
        try:
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            options.add_argument("--no-sandbox") # Important for running in many CI environments
            options.add_argument("--disable-dev-shm-usage")
            cls.driver = webdriver.Chrome(options=options)
        except WebDriverException as e:
            cls.tearDownClass() # Ensure cleanup is called
            raise unittest.SkipTest(f"Skipping test: ChromeDriver is not available or configured correctly. Error: {e}")


    @classmethod
    def tearDownClass(cls):
        """Shut down the server and browser."""
        if cls.server:
            cls.server.shutdown()
            cls.server.server_close()
        if cls.server_thread:
            cls.server_thread.join(timeout=2)
        if cls.driver:
            cls.driver.quit()
        # Restore the original working directory
        os.chdir(cls.original_cwd)

    def test_page_loads_and_js_executes(self):
        """Test if the page loads and the JavaScript correctly modifies the DOM."""
        if not self.driver: self.skipTest("WebDriver not available")

        self.driver.get(self.test_url)

        # 1. Verify the main title
        self.assertEqual(self.driver.title, "Hello World App")
        h1_element = self.driver.find_element(By.TAG_NAME, "h1")
        self.assertEqual(h1_element.text, "Hello World")

        # 2. Verify the JavaScript execution
        # Use WebDriverWait to wait for the element to have the expected text
        wait = WebDriverWait(self.driver, 10) # Wait up to 10 seconds
        js_message_element = wait.until(
            EC.text_to_be_present_in_element((By.ID, "js-message"), "JavaScript is working!")
        )
        self.assertTrue(js_message_element, "JavaScript did not set the expected message.")

    def test_directory_traversal_is_blocked(self):
        """Test to ensure directory traversal is not possible."""
        if not self.driver: self.skipTest("WebDriver not available")

        # Selenium cannot directly check status codes easily for navigation attempts.
        # Instead, we check that navigating to a forbidden URL does not display the
        # content of the forbidden resource. A 404 page will have a different title
        # and content than the file we are trying to access.
        forbidden_url = f"{self.test_url}/../main.py"
        self.driver.get(forbidden_url)

        # A 404 page from SimpleHTTPRequestHandler will contain "Error response" in the title
        # and "File not found" in the body.
        self.assertIn("Error response", self.driver.title)
        self.assertIn("File not found", self.driver.page_source)
        # Ensure the source of main.py is not in the page
        self.assertNotIn("import http.server", self.driver.page_source)


if __name__ == '__main__':
    unittest.main()