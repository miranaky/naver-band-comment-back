import time
from pathlib import Path

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

BANDID = "93879777"
POSTID = "3"


current_path = Path(__file__).parent.absolute()

options = Options()
options.add_argument("disable_extensions")
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
options.add_argument(f"--user-agent={user_agent}")
options.add_argument(f"--user-data-dir={current_path.joinpath('user_data')}")
# options.add_argument("--headless")
# options.add_experimental_option("detach", True)

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://band.us/")

time.sleep(0.5)
# driver cookie exist check

_cookies = driver.get_cookies()
if not _cookies:
    print("cookie not exist")

driver.get(f"https://band.us/band/{BANDID}")
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (
            By.XPATH,
            '//*[@data-viewname="DPostListView" and contains(@class, "postWrap")]',
        )
    )
)
# Scroll to the bottom of the page to load more items

post_list_html = driver.execute_script("return document.documentElement.outerHTML;")
soup = BeautifulSoup(post_list_html, "lxml")
divs = soup.find_all("div", class_="postListInfoWrap")

a_tags = []
for div in divs:
    a_tag = div.find(
        "a",
        href=lambda href: href
        and href.startswith(f"https://band.us/band/{BANDID}/post/"),
    )
    if a_tag is not None:
        a_tags.append(a_tag.get("href"))
