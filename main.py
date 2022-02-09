from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import time

DRIVER_PATH = "E:\Softwares\Chromedriver\chromedriver.exe"
ZILLOW_URL = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D"
GOOGLE_FORM_USER = 'https://docs.google.com/forms/d/e/1FAIpQLScnGgGMfRUq56HuJdbS6atw8mau71Ioyv4Bwo9bDNGbTxdUqQ/viewform?usp=sf_link'
GOOGLE_FORM_ADMIN = "https://docs.google.com/forms/d/1KEa4PEoBn95y-rebbWYLhMIMjlTiSyQWtTv5qgx-_O8/edit?usp=sharing&hl=en"


# ------------------------------- Using Requests To Get Data From Zillow Website ---------------------------------------
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.8',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}
response = requests.get(url=ZILLOW_URL, headers=headers)
content = response.text

# ------------------------------- Using Beautiful Soup To Parse The HTML And Manage Our Data ---------------------------
soup = BeautifulSoup(content, "html.parser")
house_links_elements = soup.select(".list-card-info a")
house_addresses_elements = soup.select(".list-card-info a address")
house_prices_elements = soup.select(".list-card-info .list-card-price")
house_links = []
house_addresses = []
house_prices = []
for each in house_links_elements:
    href = each['href']
    if href.startswith("/b"):
        href = f"https://www.zillow.com{href}"
    house_links.append(href)
for each in house_addresses_elements:
    address = each.text
    house_addresses.append(address)
for each in house_prices_elements:
    price = each.text
    house_prices.append(price)
print(house_links)
print(house_addresses)
print(house_prices)

# --------------------------------------- Using Selenium To Fill Out Google Form With Our Data -------------------------
service = Service(executable_path=DRIVER_PATH)
driver = webdriver.Chrome(service=service)
driver.get(GOOGLE_FORM_USER)
time.sleep(2)
for house in range(len(house_addresses)):
    address_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span')
    address_input.send_keys(house_addresses[house])
    price_input.send_keys(house_prices[house])
    link_input.send_keys(house_links[house])
    submit.click()
    time.sleep(1)
    submit_another = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    submit_another.click()
    time.sleep(1)

# --------------------------------------- Using Selenium To Download Results Sheet -------------------------------------
driver.get(GOOGLE_FORM_ADMIN)
time.sleep(2)
responses = driver.find_element(By.XPATH, '//*[@id="tJHJj"]/div[3]/div[1]/div/div[2]/span/div')
responses.click()
time.sleep(2)
more_options = driver.find_element(By.XPATH, '//*[@id="ResponsesView"]/div/div[1]/div[1]/div[2]/div[2]/div/div/span')
more_options.click()
time.sleep(2)
download_sheet = driver.find_element(By.XPATH, '//*[@id="wizViewportRootId"]/div[9]/div/div/span[4]/div[3]/div')
download_sheet.click()
time.sleep(4)

