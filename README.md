# BrowserStack Parallel News Scraper

This project demonstrates Selenium automation, web scraping, translation API integration, and parallel cross-browser testing using BrowserStack.

## Features

- Scrapes first 5 articles from El País Opinion section
- Extracts Spanish titles and content
- Translates titles to English using deep-translator
- Downloads article cover images
- Performs word frequency analysis
- Executes tests locally and on BrowserStack
- Runs tests in parallel across multiple browsers

## Technologies Used

- Python
- Selenium
- BrowserStack Automate
- deep-translator API
- Multithreading

## Cross Browser Testing

Tested on:

- Chrome (Windows)
- Firefox (Windows)
- Edge (Windows)
- Safari (Mac)
- Chrome (Mac)

## Project Structure

browserstack/
│
├── browserstack_parallel.py
├── main_local.py
├── requirements.txt
├── README.md
└── article_images/

## Setup Instructions

### Install dependencies

## How to Run

### Local Execution

```bash
python main_local.py
```

### Run on BrowserStack

```bash
python browserstack_parallel.py
```

Update your credentials in:

browserstack_parallel.py

USERNAME = "your_username"
ACCESS_KEY = "your_access_key"
