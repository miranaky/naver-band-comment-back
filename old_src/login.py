# import pickle
import sys
import time
from pathlib import Path

# from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

current_path = Path(__file__).parent.absolute()

options = Options()
options.add_argument("disable_extensions")
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
options.add_argument(f"--user-agent={user_agent}")
options.add_argument(f"--user-data-dir={current_path.joinpath('user_data')}")
options.add_experimental_option("detach", True)


service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://band.us/")

_cookies = driver.get_cookies()
print(_cookies)

driver.get(
    "https://auth.band.us/login_page?next_url=https%3A%2F%2Fband.us%2Fhome%3Freferrer%3Dhttps%253A%252F%252Fband.us%252F"
)
time.sleep(1)
driver.find_element(By.CSS_SELECTOR, "label > span").click()
driver.find_element(By.CSS_SELECTOR, "#email_login_a > .text").click()
time.sleep(1)
driver.find_element(By.ID, "input_email").send_keys("smkang0321@gmail.com")
time.sleep(1)
driver.find_element(By.CSS_SELECTOR, ".uBtn").click()
actions = ActionChains(driver)

driver.find_element(By.ID, "pw").click()
driver.find_element(By.ID, "pw").send_keys("cjdfyd2024!")
driver.find_element(By.ID, "pw").send_keys(Keys.ENTER)
time.sleep(3)
WebDriverWait(driver, sys.maxsize).until(
    lambda driver: driver.current_url == "https://band.us/"
)

_cookies = driver.get_cookies()
print(_cookies)
driver.quit()
