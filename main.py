import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
import pandas as pd
from datetime import datetime
import time
import pdfkit
import os
from pdf_scrape import download_special_pdf


def set_driver(show_browser=False):
    profile = {"plugins.plugins_list": [{"enabled": False,"name": "Chrome PDF Viewer"}],
               "download.default_directory": "C:/Users/91884/OneDrive/Desktop/pdf_scraping", #change this path
               "download.extensions_to_open": ""}
    options = Options()
    if not show_browser:
        options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_experimental_option("prefs", profile)
    try:
        service = Service('chromedriver.exe')
        chrome_driver = webdriver.Chrome(service=service, options=options)
        return chrome_driver
    except WebDriverException as e:
        return None

def is_pdf_link(url):
    response = requests.get(url, stream=True)
    time.sleep(3)
    if response.status_code == 200:
        content_type = response.headers.get('content-type')

        if 'pdf' in content_type.lower():
            try:
                magic_number = response.raw.read(4)
                is_pdf = magic_number == b'%PDF'
                return is_pdf
            except Exception:
                pass

    return False


def get_link(url: str):
    driver = set_driver(show_browser=True)
    try:
        driver.get(url)
        pdf_url = driver.current_url
        # print(pdf_url)
        if pdf_url == url:
            iframe = driver.find_element(By.TAG_NAME, "iframe")
            pdf_url = iframe.get_attribute("src")
            # print(pdf_url)
        return pdf_url
    finally:
        driver.quit()

def download_pdf(url):
    response = requests.get(url)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{timestamp}.pdf"
    file_path = os.path.join('./PDFS', filename)
    with open(file_path, "wb") as f:
        f.write(response.content)
    file_names[url] = filename
    print(file_names[url], "for", url)

def download_webpage(url):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{timestamp}.pdf"
    file_path = os.path.join('./PDFS', filename)
    pdfkit.from_url(url, file_path)
    file_names[url] = filename
    print(file_names[url], "for", url)

df = pd.read_excel('06062023.xlsx')#----------------------------excel file---------------------
urls = list(df.loc[:, 'FactsURL'])
file_names = dict()

for url in ['https://www.getonpointenergy.com/api/efl/1-54254-12-Houston-CenterPoint']:
    if  'bit.ly/' in url and requests.get(url, stream=True).status_code == 403:
        file_names[url] = "NAN"
        print(file_names[url], "for", url)
        continue
    try:
        if is_pdf_link(url):
            download_pdf(url)
        else:
            download_pdf(get_link(url))
    except:
        try:
            download_webpage(url)
        except:
            try:
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                filename = f"{timestamp}.pdf"
                download_special_pdf(url, filename) 
                file_names[url] = filename
                print(file_names[url], "for", url)
            except:
                file_names[url] = "NAN"
                print(file_names[url], "for", url)
print(file_names)
print(len(file_names))

# try:
#     df['filename'] = list(file_names.values())
#     df.to_excel('06062023.xlsx', index=False)
#     print("filename add to excel file successfully")
# except:
#     print("pdfs scrape successfully but can not able to add in given excel file so it store in filename.xlsx file")
#     filenames_df = pd.DataFrame(list(file_names.items()), columns=['urls', 'filenames'])
#     filenames_df.to_excel('filenames.xlsx')

