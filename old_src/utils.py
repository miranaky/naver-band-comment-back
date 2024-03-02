def save_current(driver):
    html = driver.execute_script("return document.documentElement.outerHTML;")

    with open("band_93879777.html", "w") as f:
        f.write(html)
