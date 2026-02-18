import os
import re
import time
import requests
from collections import Counter

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager
from deep_translator import GoogleTranslator


# ===============================
# CREATE IMAGE FOLDER
# ===============================

IMAGE_DIR = "article_images"

if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)


# ===============================
# SETUP DRIVER
# ===============================

def setup_driver():

    chrome_options = Options()

    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--lang=es")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    return driver


# ===============================
# ACCEPT COOKIES FUNCTION
# ===============================

def accept_cookies(driver):

    try:

        wait = WebDriverWait(driver, 10)

        cookie_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(., 'Aceptar')]")
            )
        )

        cookie_button.click()

        print("Cookies accepted.")

        time.sleep(2)

    except:

        print("Cookie popup not found or already accepted.")


# ===============================
# DOWNLOAD IMAGE FUNCTION
# ===============================

def download_image(url, index):

    try:

        response = requests.get(url, stream=True, timeout=10)

        if response.status_code == 200:

            filename = os.path.join(
                IMAGE_DIR,
                f"article_{index}.jpg"
            )

            with open(filename, "wb") as file:

                for chunk in response.iter_content(1024):
                    file.write(chunk)

            print(f"Image saved: {filename}")

        else:

            print("Image not accessible.")

    except Exception as e:

        print("Image download failed:", e)


# ===============================
# SCRAPE ARTICLES FUNCTION
# ===============================

def scrape_articles(driver):

    wait = WebDriverWait(driver, 10)

    # Open homepage
    driver.get("https://elpais.com")

    accept_cookies(driver)

    # Go to Opinion section
    driver.get("https://elpais.com/opinion/")

    # Wait for articles
    article_elements = wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "article h2 a")
        )
    )

    # FIX: Store links instead of elements (prevents stale error)
    article_links = []

    for elem in article_elements[:5]:

        link = elem.get_attribute("href")

        if link:
            article_links.append(link)

    translated_titles = []

    # Visit each article
    for index, link in enumerate(article_links, start=1):

        driver.get(link)

        wait.until(
            EC.presence_of_element_located(
                (By.TAG_NAME, "h1")
            )
        )

        # ===============================
        # GET TITLE
        # ===============================

        title = driver.find_element(
            By.TAG_NAME,
            "h1"
        ).text

        print("\n==============================")
        print(f"Article {index} Title (Spanish):")
        print(title)

        # ===============================
        # GET CONTENT
        # ===============================

        paragraphs = driver.find_elements(
            By.CSS_SELECTOR,
            "article p"
        )

        print("\nContent (Spanish):")

        for p in paragraphs[:5]:

            text = p.text.strip()

            if text:
                print(text)

        # ===============================
        # DOWNLOAD IMAGE
        # ===============================

        try:

            img = driver.find_element(
                By.CSS_SELECTOR,
                "figure img"
            )

            img_url = img.get_attribute("src")

            if img_url:

                download_image(
                    img_url,
                    index
                )

            else:

                print("No image URL found.")

        except:

            print("No cover image found.")

        # ===============================
        # TRANSLATE TITLE
        # ===============================

        translated = GoogleTranslator(
            source="es",
            target="en"
        ).translate(title)

        translated_titles.append(translated)

        print("\nTranslated Title (English):")
        print(translated)

    return translated_titles


# ===============================
# WORD ANALYSIS FUNCTION
# ===============================

def analyze_titles(translated_titles):

    print("\n==============================")
    print("WORD FREQUENCY ANALYSIS")

    words = []

    for title in translated_titles:

        extracted = re.findall(
            r'\b[a-zA-Z]+\b',
            title.lower()
        )

        words.extend(extracted)

    counter = Counter(words)

    repeated_words = {
        word: count
        for word, count in counter.items()
        if count > 2
    }

    if repeated_words:

        print("\nWords repeated more than twice:")

        for word, count in repeated_words.items():

            print(f"{word}: {count}")

    else:

        print("No words repeated more than twice.")


# ===============================
# MAIN FUNCTION
# ===============================

def main():

    driver = setup_driver()

    try:

        translated_titles = scrape_articles(driver)

        analyze_titles(translated_titles)

    finally:

        driver.quit()


# ===============================
# ENTRY POINT
# ===============================

if __name__ == "__main__":

    main()
