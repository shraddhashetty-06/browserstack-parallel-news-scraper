"""
BrowserStack Parallel Execution Script
Author: Shraddha Shetty

This script:
• Runs tests in parallel on BrowserStack
• Opens El País Opinion page
• Scrapes first 5 articles
• Translates titles to English
• Downloads cover images
• Performs word frequency analysis
• Saves results locally
"""

import threading
import requests
import os
import re
from collections import Counter
from deep_translator import GoogleTranslator
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# ==============================
# BrowserStack Credentials
# ==============================

USERNAME = "shraddhashetty_DSfsiQ"
ACCESS_KEY = "WQoM2zhfeZPXGV62PS6j"

URL = f"https://{USERNAME}:{ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"

# ==============================
# Browser configurations
# ==============================

browsers = [
    {"browserName": "Chrome", "browserVersion": "latest", "os": "Windows", "osVersion": "11"},
    {"browserName": "Firefox", "browserVersion": "latest", "os": "Windows", "osVersion": "10"},
    {"browserName": "Edge", "browserVersion": "latest", "os": "Windows", "osVersion": "11"},
    {"browserName": "Safari", "browserVersion": "latest", "os": "OS X", "osVersion": "Ventura"},
    {"browserName": "Chrome", "browserVersion": "latest", "os": "OS X", "osVersion": "Monterey"}
]

# ==============================
# Create folder for images
# ==============================

if not os.path.exists("article_images"):
    os.makedirs("article_images")

# ==============================
# Translation function
# ==============================

def translate_text(text):
    try:
        return GoogleTranslator(source='auto', target='en').translate(text)
    except:
        return text


# ==============================
# Word frequency analysis
# ==============================

def analyze_words(text):
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    freq = Counter(words)

    repeated = {word: count for word, count in freq.items() if count > 2}

    print("\nWord Frequency Analysis:")
    if repeated:
        for word, count in repeated.items():
            print(f"{word}: {count}")
    else:
        print("No words repeated more than twice.")


# ==============================
# Scraper function
# ==============================

def scrape_articles(driver):

    print("\nScraping articles...\n")

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    articles = soup.find_all("article")[:5]

    full_text = ""

    for index, article in enumerate(articles, start=1):

        title_tag = article.find("h2")

        title = title_tag.get_text(strip=True) if title_tag else "No title"

        print(f"\nArticle {index} Title (Spanish):")
        print(title)

        translated = translate_text(title)

        print("\nTranslated Title (English):")
        print(translated)

        full_text += translated + " "

        # image download
        img_tag = article.find("img")

        if img_tag and img_tag.get("src"):
            img_url = img_tag["src"]

            try:
                img_data = requests.get(img_url).content

                file_path = f"article_images/article_{index}.jpg"

                with open(file_path, "wb") as f:
                    f.write(img_data)

                print(f"Image saved: {file_path}")

            except:
                print("Image download failed")

        else:
            print("No cover image found")

    analyze_words(full_text)


# ==============================
# BrowserStack Test Function
# ==============================

def run_test(cap):

    options = Options()

    options.set_capability("browserName", cap["browserName"])
    options.set_capability("browserVersion", cap["browserVersion"])

    options.set_capability("bstack:options", {
        "os": cap["os"],
        "osVersion": cap["osVersion"],
        "sessionName": "El Pais Scraper Test",
        "buildName": "BrowserStack Python Parallel",
        "source": "browserstack-python"
    })

    driver = webdriver.Remote(
        command_executor=URL,
        options=options
    )

    print(f"\nStarted session on {cap['browserName']}")

    driver.get("https://elpais.com/opinion/")

    scrape_articles(driver)

    driver.quit()

    print(f"Finished session on {cap['browserName']}")


# ==============================
# Parallel Execution
# ==============================

threads = []

for cap in browsers:
    thread = threading.Thread(target=run_test, args=(cap,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

print("\nAll parallel sessions completed.")
