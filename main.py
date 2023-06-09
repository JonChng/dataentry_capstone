import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import lxml
import time

chromedriver_path = "/Users/jonathanchng/Downloads/chromedriver_mac64/chromedriver"


listings_endpoint = "https://www.zillow.com/homes/for_rent/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-122.63417281103516%2C%22east%22%3A-122.23248518896484%2C%22south%22%3A37.66150047215739%2C%22north%22%3A37.888907562841936%7D%2C%22mapZoom%22%3A12%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D"
headers = {
    "Accept-Language":"en-GB,en;q=0.7",
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
}
data = requests.get(listings_endpoint, headers=headers)
data.raise_for_status()
print(data)

form = "https://forms.gle/86b7CqqowP8JnG3p6"

soup = BeautifulSoup(data.text, 'html.parser')

listings = soup.find_all("li", {"class":"ListItem-c11n-8-85-1__sc-10e22w8-0 srp__sc-wtsrtn-0 jhnswL with_constellation"})
to_remove = []

#Getting Links and removing listings with no links
links = []
prices = []
addresses =[]


for i in listings:
    a = i.find_next("a", {"class":"property-card-link"})

    try:
        link = a['href']
        addition = link.split("/b/")[1]
        link_url = "https://www.zillow.com/b/" + addition
        links.append(link_url)


    except TypeError:
        print("No Link.")
        to_remove.append(i)

listings = [x for x in listings if x not in to_remove]

#Getting Prices

for i in listings:
    a = i.find_next("span")
    prices.append(a.text)

#Getting Addresses
for i in listings:
    a = i.find_next("address")
    addresses.append(a.text)


for i in range(len(listings)):
    driver = webdriver.Chrome(chromedriver_path)
    driver.get(form)

    time.sleep(10)

    address = addresses[i]
    price = prices[i]
    link = links[i]

    add_ = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    add_.send_keys(address)

    price_ = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_.send_keys(price)

    link_ = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_.send_keys(link)

    driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div').click()







