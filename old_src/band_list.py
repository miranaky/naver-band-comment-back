import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

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
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "ul.bandCardList.gMab25"))
)
elements = driver.find_elements(By.CSS_SELECTOR, "a.bandCover._link:not(._adBandCover)")

for band in elements:
    band_url = band.get_attribute("href")
    band_name = band.find_element(By.CSS_SELECTOR, "div.bandName p.uriText")
    print(band_url)
    print(band_name.text)
