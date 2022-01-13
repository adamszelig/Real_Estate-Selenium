from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
import time

import requests
import lxml
from bs4 import BeautifulSoup

path = "C:/Users/Adam/PycharmProjects/S48_Selenium/chromedriver_win32/chromedriver_old.exe"
ZILLOW = "https://www.zillow.com/san-francisco-ca/rentals/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22San%20Francisco%2C%20CA%22%2C%22mapBounds%22%3A%7B%22west%22%3A-122.63417281103516%2C%22east%22%3A-122.23248518896484%2C%22south%22%3A37.662044042279824%2C%22north%22%3A37.88836565815623%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A20330%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A897707%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D"
FORM = "https://docs.google.com/forms/d/e/1FAIpQLScyiRfpqcg1sqxiK9sE91tWzhSI53t86MoVvhIS0KsK48lMNA/viewform?usp=sf_link"


class PropertySearch:

    def __init__(self):
        self.data = []

    def get_properties(self, path):
        print("Zillow request initialized")
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
            "Accept-Language": "hu-HU,hu;q=0.9,en;q=0.8"
        }
        response = requests.get(path, headers=header)
        # print(response.text)

        soup = BeautifulSoup(response.text, "lxml")
        # print(soup.prettify())
        price = soup.select(selector=".list-card-info .list-card-price")
        address = soup.select(selector=".list-card-info .list-card-addr")
        link = soup.select(selector=".list-card-info .list-card-link")
        price = [p.text for p in price]
        address = [a.text for a in address]
        link = [l.get("href") for l in link]
        for l in link:
            if "zillow" not in l:
                link[link.index(l)] = "https://www.zillow.com/"+l
        print(len(price), len(address), len(link))
        print(price)
        print(address)
        print(link)
        for i in range(len(price)):
            self.data.append({"price": price[i], "address": address[i], "link": link[i]})
        # print(self.data)
        print("Finished Zillow data read out")

    def google_form(self, path, FORM):
        print("Google form opening initialized")
        print("self.s = Service(path)")
        self.s = Service(path)
        print("self.driver = webdriver.Chrome(service=self.s)")
        self.driver = webdriver.Chrome(service=self.s)
        # self.driver.maximize_window()
        print("self.driver.get(FORM)")
        self.driver.get(FORM)
        time.sleep(6)
        for d in self.data:
            property_input = self.driver.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
            property_input.send_keys(d["address"])
            price_input = self.driver.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
            price_input.send_keys(d["price"])
            link_input = self.driver.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
            link_input.send_keys(d["link"])
            time.sleep(0.5)
            button = self.driver.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')
            button.click()
            time.sleep(1)
            button_next = self.driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
            button_next.click()
            time.sleep(1)
        print("Finished")

agent = PropertySearch()
agent.get_properties(ZILLOW)
agent.google_form(path, FORM)

