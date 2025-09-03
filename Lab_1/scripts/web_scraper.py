#Code for web scraping the given cnbc url

#import required libraries
from pathlib import Path
from shutil import which
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#URL to scrap
URL = "https://www.cnbc.com/world/?region=world"
RAW_FILE = Path("../data/raw_data/web_data.html")
print("Scrapping the given url")
# This is because of snap installation of firefox
FF_SNAP_BIN = "/snap/firefox/current/usr/lib/firefox/firefox"

def main():
    opts = Options()
    opts.add_argument("-headless")
    if Path(FF_SNAP_BIN).exists():
        opts.binary_location = FF_SNAP_BIN
    driver = webdriver.Firefox(service=Service(which("geckodriver") or "/usr/bin/geckodriver"),options=opts,)

    try:
        driver.get(URL)

        #Handling the cookies popup
        #This part was refered from stackoverflow
        try:
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))).click()
        except Exception:
            pass

        # Wait for page loading
        WebDriverWait(driver, 20).until(lambda d: d.execute_script("return document.readyState") == "complete")
        driver.execute_script("window.scrollBy(0, 600);")
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR,"[class*='MarketsBanner'], div.MarketsBanner-marketData,""a.MarketCard-container, [data-symbol]")))

        # Saving the raw html file
        banner = f"<!-- downloaded_at={datetime.now():%Y-%m-%d %H:%M:%S} url={URL} -->\n"
        RAW_FILE.write_text(banner + driver.page_source, encoding="utf-8")
        print(f"Scrapping complete. Saved HTML → {RAW_FILE.resolve()}")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()

