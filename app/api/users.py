import sys
import time
from typing import Optional

from fastapi import APIRouter, Depends
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from app.core.driver import get_browser_driver, get_driver

router = APIRouter()


@router.post("/login")
async def login(
    user_id: Optional[str] = "smkang0321@gmail.com",
    user_pw: Optional[str] = "cjdfyd2024!!",
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

    _cookies = driver.get_cookies()
    print(_cookies)


@router.get("/profile")
async def get_my_profile(driver=Depends(get_driver)):
    driver.get("https://band.us/my/profiles/1")
    profile_info = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.profileInfo"))
    )
    profile_name = profile_info.find_element(By.CLASS_NAME, "profileName").text
    return profile_name
