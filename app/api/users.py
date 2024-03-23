import sys
import time
from typing import Optional

from fastapi import APIRouter, Body, Depends
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from app.core.driver import get_browser_driver, get_driver
from app.core.driver import get_browser_driver, get_driver

router = APIRouter()


@router.post("/login")
async def login(
    user_id: Optional[str] = Body(None),  # "smkang0321@gmail.com",
    user_pw: Optional[str] = Body(None),  # "cjdfyd2024!!",
    driver=Depends(get_browser_driver),
):
    driver.get("https://band.us/")

    _cookies = driver.get_cookies()
    print(_cookies)

    driver.get(
        "https://auth.band.us/login_page?next_url=https%3A%2F%2Fband.us%2Fhome%3Freferrer%3Dhttps%253A%252F%252Fband.us%252F"
    )
    time.sleep(1)
    if user_id and user_pw:
        driver.find_element(By.CSS_SELECTOR, "label > span").click()
        driver.find_element(By.CSS_SELECTOR, "#email_login_a > .text").click()
        time.sleep(1)
        driver.find_element(By.ID, "input_email").send_keys(user_id)
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, ".uBtn").click()

        driver.find_element(By.ID, "pw").click()
        driver.find_element(By.ID, "pw").send_keys(user_pw)
        driver.find_element(By.ID, "pw").send_keys(Keys.ENTER)
        time.sleep(3)

    if driver.current_url != "https://band.us/":
        driver.find_element(By.ID, "trust").click()
    WebDriverWait(driver, sys.maxsize).until(
        lambda driver: driver.current_url == "https://band.us/"
    )


@router.get("/profile")
async def get_my_profile(driver=Depends(get_driver)):
    try:
        driver.get("https://band.us/my/profiles/1")
        profile_info = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.profileInfo"))
        )
        profile_name = profile_info.find_element(By.CLASS_NAME, "profileName").text
        return True
    except TimeoutException:
        return False


@router.delete("/logout")
async def logout(driver=Depends(get_driver)):
    driver.get("https://band.us/")
    try:
        header_widget_area = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "headerWidgetArea"))
        )
    except TimeoutException:
        return "logout"
    header_widget_area.find_element(
        By.CSS_SELECTOR, "button.btnMySetting._btnMySetting._btnWidgetIcon"
    ).click()
    logout_button = driver.find_element(
        By.CSS_SELECTOR, "a.menuModalLink._btnLogout"
    ).click()
    # 로그아웃 확인 창을 찾습니다.
    logout_confirm = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.lyContent"))
    )

    # 로그아웃 버튼을 찾고 클릭합니다.
    logout_button = logout_confirm.find_element(
        By.CSS_SELECTOR, "button.uButton.-confirm._btnLogout"
    )
    logout_button.click()
    return "logout"
