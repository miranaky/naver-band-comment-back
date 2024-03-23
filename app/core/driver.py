import random
from contextlib import contextmanager
from pathlib import Path

from models import CreateComment
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

current_path = Path(__file__).parent.absolute()

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
]


@contextmanager
def headless_webdriver_context():
    options = Options()
    options.add_argument("disable_extensions")
    user_agent = random.choice(user_agents)
    options.add_argument(f"--user-agent={user_agent}")
    options.add_argument(f"--user-data-dir={current_path.joinpath('user_data')}")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("window-size=1920x1080")  # 해상도
    options.add_argument("--log-level=0")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    try:
        yield driver
    finally:
        driver.quit()


@contextmanager
def webdriver_context():
    _options = Options()
    _options.add_argument("disable_extensions")
    _user_agent = random.choice(user_agents)
    _options.add_argument(f"--user-agent={_user_agent}")
    _options.add_argument(f"--user-data-dir={current_path.joinpath('user_data')}")

    browser_driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=_options
    )
    try:
        yield browser_driver
    finally:
        browser_driver.quit()


def get_driver(
    new_comment: CreateComment,
):
    if new_comment.view:
        with webdriver_context() as browser_driver:
            yield browser_driver
    else:
        with headless_webdriver_context() as driver:
            yield driver


def get_browser_driver():
    with webdriver_context() as browser_driver:
        yield browser_driver
