from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import random
import os
import time

class Snapchat:
    def __init__(self, path_delay=5, driver_arguments=None):
        self.path_delay = path_delay
        if driver_arguments is None:
            driver_arguments = []
        self.driver_arguments = [
            "--window-size=1920,1080",
            "--disable-gpu",
            "--start-maximized",
            "--no-sandbox",
            "--enable-unsafe-swiftshader",  # Add this flag for WebGL issues
            f"--user-data-dir={os.path.join(os.path.dirname(__file__), 'driver')}"
        ]
        self.driver_arguments.extend(driver_arguments)
        
    def driver(self):
        options = webdriver.ChromeOptions()
        for option in self.driver_arguments:
            options.add_argument(option)
        
        # Automatically download and manage ChromeDriver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.get("https://web.snapchat.com/")
        return driver
    
    def farm_points(self):
        driver = self.driver()
        wait = WebDriverWait(driver, self.path_delay)

        # Update these selectors based on Snapchat's current DOM structure
        friends_path = (By.CLASS_NAME, "O4POs")  # Update if class names change
        snap_take_button_path = driver.find_element(By.XPATH, "//svg/path")
        button = wait.until(EC.element_to_be_clickable((By.XPATH, "//svg[@aria-label='Unselect chosen user']")))
        send_button = driver.find_element(By.XPATH, "//button[.//svg[@width='16' and @height='16']]")
        confirm_snap_path = (By.XPATH, "//button[contains(text(), 'Send')]")

        driver.get("https://web.snapchat.com/")

        while True:
            try:
                # Locate all friends in the list
                friends = wait.until(EC.presence_of_all_elements_located(friends_path))
                for user in friends:
                    try:
                        user.click()

                        # Click "Take Snap" button
                        snap_button = wait.until(EC.element_to_be_clickable(snap_take_button_path))
                        snap_button.click()

                        # Select a random snap (if multiple options exist)
                        snaps = wait.until(EC.presence_of_all_elements_located(take_snap_path))
                        random.choice(snaps).click()

                        # Select users to send to
                        users = wait.until(EC.presence_of_all_elements_located(choice_users_path))
                        for recipient in users[:3]:  # Limit to 3 recipients for testing
                            recipient.click()

                        # Confirm sending the snap
                        send_button = wait.until(EC.element_to_be_clickable(confirm_snap_path))
                        send_button.click()

                        print("Snap sent successfully.")

                        # Pause to avoid being flagged for spam
                        time.sleep(random.randint(2, 5))
                    except Exception as user_error:
                        print(f"Error with user interaction: {user_error}")
                        continue
            except Exception as e:
                print(f"An error occurred: {e}")
                # Perform a fallback action
                action_chains = ActionChains(driver)
                html_element = driver.find_element(By.TAG_NAME, "html")
                action_chains.move_to_element_with_offset(html_element, 0, 0).click().perform()

if __name__ == "__main__":
    try:
        snapchat = Snapchat()
        snapchat.farm_points()
    except Exception as main_error:
        print(f"Critical error: {main_error}")
