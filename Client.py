import socket
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

HOST = "127.0.0.1"
PORT = 65432
URL = ""

AMOUNT_BROWSERS = 2

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

def setup_browser():
    print("setting browser...")
    browser = webdriver.Chrome(options=chrome_options)
    if URL == "":
        browser.get(f"http://{HOST}:{PORT}")
    else:
        browser.get(URL)


threads = []

for i in range(AMOUNT_BROWSERS):
    browser_thread = threading.Thread(target=setup_browser)
    threads.append(browser_thread)

for t in threads:
    t.start()
    t.join()