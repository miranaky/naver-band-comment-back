import pickle
import sys
import time
from pathlib import Path

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

current_path = Path(__file__).parent.absolute()

options = Options()
options.add_argument("disable_extensions")
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
options.add_argument(f"--user-agent={user_agent}")
options.add_argument(f"--user-data-dir={current_path.joinpath('user_data')}")
options.add_experimental_option("detach", True)


service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

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
pickle.dump(
    driver.get_cookies(), open("band_cookies.pkl", "wb")
)  # 최초 로그인 후 쿠키 저장시에만

driver.get("https://band.us/band/90379433/post/2623")
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "postMain"))
)
html = driver.execute_script("return document.documentElement.outerHTML;")
# save html to file
with open("band_93879777.html", "w") as f:
    f.write(html)
time.sleep(60)
soup = BeautifulSoup(html, "lxml")
print(soup.prettify())


# driver.find_element(By.CSS_SELECTOR, ".cCard:nth-child(1) .postSet").click()
# driver.find_element(By.LINK_TEXT, "주소 복사").click()


# session = requests.Session()
# headers = {
#     "User-Agent": user_agent,
# }
# session.headers.update(headers)
# for cookie in _cookies:
#     session.cookies.set(cookie["name"], cookie["value"])

# response = session.get("https://band.us/band/93879777")
# soup = BeautifulSoup(response.text, "lxml")
# print(soup.prettify())
