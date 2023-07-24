from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time
import pyautogui
from datetime import datetime

# Replace this your folder where you want to store pdf
download_folder = r'C:\Users\91884\OneDrive\Desktop\pdf_scraping\PDFS'

if not os.path.exists(download_folder):
    os.makedirs(download_folder)

chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
    "plugins.always_open_pdf_externally": False,  
    "download.default_directory": download_folder,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})


def download_special_pdf(url, filename):
    try :
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        time.sleep(5)
        pyautogui.hotkey('ctrl', 's')  # Replace 'ctrl' with 'cmd' for Mac
        time.sleep(2)
        pyautogui.typewrite(os.path.join(download_folder, filename))
        pyautogui.press('enter')
        time.sleep(2)
        pyautogui.press('enter')
        time.sleep(6)

    finally:
        driver.quit()

