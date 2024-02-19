import os
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

path = os.path.dirname(os.path.abspath(__file__))


options = Options()
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
options.add_argument(f"user-agent={user_agent}")

options.add_argument("--headless")
# options.add_argument("--disable-gpu")

options.add_experimental_option("detach", True)
options.add_experimental_option("excludeSwitches", ["enable-logging"])


service = Service(ChromeDriverManager(path=f"{path}/driver").install())
driver = webdriver.Chrome(service=service, options=options)

start_time = time.time()
driver.get("https://band.us/band/72182334")
time.sleep(3)

for i in range(3):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(0.5)
print("end of scroll :", time.time() - start_time)
html = driver.page_source

soup = BeautifulSoup(html, "html.parser")
# post_wrap = soup.find_all("div", class_="postWrap")
post_list = soup.find_all("div", class_="cCard gContentCardShadow")

for post in post_list:
    post_info = post.find("div", class_="postListInfoWrap")
    if post_info:
        url = post_info.find("a", class_="time", href=True)["href"]
        created_at = post_info.find("time").text
        text_body = post.find("p", class_="txtBody")

        print(f"url: {url}")
        print(f"created_at: {created_at}")
        print(f"text_body: {text_body}")

# for idx, post in enumerate(post_wrap):
#     with open(f"test{idx}.html", "w") as f:
#         f.write(str(post))
#         print(type(post))

driver.quit()
print("process time: ", time.time() - start_time)
