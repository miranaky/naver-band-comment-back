import random
import time
from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from utils import save_current

BANDID = "90379433"
POSTID = "2675"


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

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
]

options = Options()
options.add_argument("disable_extensions")
user_agent = random.choice(user_agents)
options.add_argument(f"--user-agent={user_agent}")
options.add_argument(f"--user-data-dir={current_path.joinpath('user_data')}")
# options.add_argument("--headless=new")


service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://band.us/")

time.sleep(0.5)
# driver cookie exist check
_cookies = driver.get_cookies()
if not _cookies:
    print("cookie not exist")


driver.get(f"https://band.us/band/{BANDID}/post/{POSTID}")
comment_start = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "dPostCommentMainView"))
)

number_of_comments_div = driver.find_element(
    By.CSS_SELECTOR, "span.comment._commentCountBtn.gCursorDefault span.count"
)
number_of_comments = int(number_of_comments_div.text)

start_time = time.time()

if number_of_comments > 10:
    click_first_comment_button(driver)
    click_more_comment_button(driver)

end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")

my_comment = ".."

save_current(driver)


comment_divs = driver.find_elements(By.CSS_SELECTOR, "div.cComment")
count = 0
while count < 2:
    comment_divs = driver.find_elements(By.CSS_SELECTOR, "div.cComment")
    if len(comment_divs) == int(number_of_comments):
        print("댓글 갯수가 일치합니다.")
        break
    print(f"댓글 갯수가 일치하지 않습니다. {len(comment_divs)} / {number_of_comments}")
    time.sleep(1)
    count += 1


driver.execute_script("arguments[0].scrollIntoView(true);", comment_start)
# 댓글을 입력한 사용자의 이름을 클릭합니다.
for idx, comment in enumerate(comment_divs):
    name_button = comment.find_element(By.CSS_SELECTOR, "button.nameWrap")
    comment_body = comment.find_element(By.CSS_SELECTOR, "p.txt._commentContent")
    time.sleep(0.1)
    driver.execute_script("arguments[0].scrollIntoView(true);", name_button)
    ActionChains(driver).move_to_element(name_button).click(name_button).perform()
    print(f"{idx+1}번째 댓글 {name_button.text} : {comment_body.text}")

# 댓글을 입력할 수 있는 textarea를 찾습니다.
input_section = driver.find_element(By.CLASS_NAME, "uInputComment")
text_area = input_section.find_element(By.TAG_NAME, "textarea")
text_area.send_keys(my_comment)
time.sleep(2)

input_section = driver.find_element(By.CLASS_NAME, "uInputComment")
# input_section html 출력
# submit 버튼을 찾습니다.
send_button = WebDriverWait(driver, 2).until(
    EC.element_to_be_clickable(
        (By.CSS_SELECTOR, ".writeSubmit.uButton._sendMessageButton.-active")
    )
)

# 버튼을 클릭합니다.
# send_button.click()
print("댓글 갯수 : ", len(comment_divs))
time.sleep(5)
driver.quit()
