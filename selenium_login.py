import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

LOGIN_URL = os.environ.get("LOGIN_URL", "https://the-internet.herokuapp.com/login")
USERNAME = os.environ.get("LOGIN_USER", "tomsmith")
PASSWORD = os.environ.get("LOGIN_PASSWORD", "SuperSecretPassword!")
HEADLESS = os.environ.get("HEADLESS", "0") == "1"


def login(driver, username, password):
    wait = WebDriverWait(driver, 10)
    driver.get(LOGIN_URL)

    wait.until(EC.visibility_of_element_located((By.ID, "username"))).send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    return wait.until(EC.visibility_of_element_located((By.ID, "flash"))).text


def main():
    options = webdriver.ChromeOptions()
    # if HEADLESS:
    #     options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=options)
    try:
        message = login(driver, USERNAME, PASSWORD)
        assert "secure area" in message, f"Login failed: {message}"
        print("Login test passed")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
