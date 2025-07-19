from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import requests
import csv

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.imdb.com/chart/top")

time.sleep(7)
titles = driver.find_elements(By.CSS_SELECTOR, value="h3.ipc-title__text")

with open("imdb_top_250.csv", mode="w", newline='', encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Rank", "Title"])

    for title in titles:
        full_text = title.text
        if ". " in full_text:
            rank, movie_title = full_text.split(". ", 1)
            writer.writerow([rank, movie_title])