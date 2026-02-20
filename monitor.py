import json
import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

BOT_TOKEN = os.getenv("8537926181:AAEYz7MtsFb47YANBNqB9De463OT1I_EuGI")
CHAT_ID = "6092781420"

SEARCH_URL = "https://www.farfetch.com/fr/shopping/men/search/items.aspx?q=prada+cup"

STATE_FILE = "state.json"

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

if os.path.exists(STATE_FILE):
    with open(STATE_FILE, "r") as f:
        state = json.load(f)
else:
    state = {}

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

print("Monitor lancé")

try:
    driver.get(SEARCH_URL)
    time.sleep(5)

    products = driver.find_elements(By.XPATH, "//a[contains(@href,'item-')]")

    links = []

    for p in products:
        link = p.get_attribute("href")
        if link and link not in links:
            links.append(link)

    for url in links:

        driver.get(url)
        time.sleep(2)

        try:
            driver.find_element(By.XPATH, "//button[contains(., 'Ajouter')]")
            current_stock = True
        except:
            current_stock = False

        old_stock = state.get(url)

        if old_stock == False and current_stock == True:

            send_message(
                f"🔥 PRADA CUP RESTOCK 🔥\n\n{url}"
            )

        state[url] = current_stock

    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

finally:
    driver.quit()
