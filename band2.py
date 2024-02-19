import pickle
import time
from pathlib import Path

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

BANDID = "93879777"
POSTID = "1"


def click_first_comment_button(driver):
    try:
        go_to_first_comment_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "goFirstComment"))
        )
        go_to_first_comment_button.click()
    except TimeoutException:
        print("No first comment button")
        pass


def click_more_comment_button(driver):
    counter = 0
    while True:
        try:
            more_comment_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "moreView"))
            )
            more_comment_button.click()
            driver.find_element(By.CLASS_NAME, "moreView")
            time.sleep(1)

        except TimeoutException:
            if counter > 2:
                print("No more comment button")
                break  # 요소가 존재하지 않으면 루프를 종료
            time.sleep(1)
            counter += 1
            continue


current_path = Path(__file__).parent.absolute()

options = Options()
options.add_argument("disable_extensions")
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
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
    cookies = pickle.load(open("band_cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)

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


driver.get(f"https://band.us/band/{BANDID}/post/{POSTID}")
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "dPostCommentMainView"))
)
start_time = time.time()

# click_first_comment_button(driver)
# click_more_comment_button(driver)

end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")

my_comment = "만나서 반가워요."

html = driver.execute_script("return document.documentElement.outerHTML;")


comment_divs = driver.find_elements(By.CSS_SELECTOR, "div.cComment")

for idx, comment in enumerate(comment_divs):
    name_button = comment.find_element(By.CSS_SELECTOR, "button.nameWrap")
    comment_body = comment.find_element(By.CSS_SELECTOR, "p.txt._commentContent")
    name_button.click()
# 댓글을 입력할 수 있는 textarea를 찾습니다.

input_section = driver.find_element(By.CLASS_NAME, "uInputComment")
text_area = input_section.find_element(By.TAG_NAME, "textarea")
text_area.send_keys(my_comment)
time.sleep(2)

input_section = driver.find_element(By.CLASS_NAME, "uInputComment")
# input_section html 출력
print(input_section.get_attribute("outerHTML"))
# submit 버튼을 찾습니다.
send_button = WebDriverWait(driver, 2).until(
    EC.element_to_be_clickable(
        (By.CSS_SELECTOR, ".writeSubmit.uButton._sendMessageButton.-active")
    )
)

# 버튼을 클릭합니다.
send_button.click()
print("댓글 갯수 : ", len(comment_divs))
time.sleep(5)
driver.quit()
