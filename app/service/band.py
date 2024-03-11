from core.driver import get_driver
from fastapi import Depends
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def get_band_list(driver=Depends(get_driver)):
    driver.get("https://band.us/")

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "ul.bandCardList.gMab25"))
    )
    elements = driver.find_elements(
        By.CSS_SELECTOR, "a.bandCover._link:not(._adBandCover)"
    )

    band_list = []
    for band in elements:
        band_url = band.get_attribute("href")
        band_name = band.find_element(By.CSS_SELECTOR, "div.bandName p.uriText").text
        band_id = band_url.split("/")[-1]
        band_list.append(
            {
                "band_url": band_url,
                "band_id": band_id,
                "band_name": band_name,
            }
        )

    return band_list
