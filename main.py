"""This is the final project on Webscraping. it is a capstone project that
 test the knowledge on beautiful soup and selenium"""
import time

GOOGLE_FORM = "https://docs.google.com/forms/d/e/1FAIpQLSe4zWuWc1hn7zOYCBqnrqTDrDopDWZBp6Uz8iiLDcX086-v1g/viewform?usp=sf_link"
ZILLOW_URL = "https://appbrewery.github.io/Zillow-Clone/"

# USE BEAUTIFUL soup to scrape all the data in the website
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.common.keys import Keys
QUESTION_1 = "//*[@id='mG61Hd']/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input"
QUESTION_2 = "//*[@id='mG61Hd']/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input"
QUESTION_3 = "//*[@id='mG61Hd']/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input"
SUBMIT = "//*[@id='mG61Hd']/div[2]/div/div[3]/div[1]/div[1]/div/span/span"


common_option = webdriver.ChromeOptions()
common_option.add_experimental_option("detach", True)

response = requests.get(url=ZILLOW_URL)
google_data = response.text


soup = BeautifulSoup(google_data, "html.parser")
# print(soup.prettify())
data = soup.find_all(name="a", class_="StyledPropertyCardDataArea-anchor")
price = soup.find_all(name="span", class_="PropertyCardWrapper__StyledPriceLine")

# Get the price, link and location
data_link = [i["href"] for i in data]

addresses = [i.text.strip().replace("\n ",'').replace("|",'') for i in data]

data_price = [i.text.strip("+/mo") for i in price]



# create a list that runs for all the address

for i in range(len(addresses)):
    try:
        new_address = addresses[i]
        i_price = data_price[i]
        i_link = data_link[i]


        print(f"ADDRESS: {new_address}, PRICE: {i_price}\nLINK: {i_link} ")

        # use SELENIUM to fill in the form created.... send all the responses to google sheet

        driver = webdriver.Chrome(common_option)
        google = driver.get(url=GOOGLE_FORM)
        question_1 = driver.find_element(By.XPATH, QUESTION_1)
        question_2 = driver.find_element(By.XPATH, QUESTION_2)
        question_3 = driver.find_element(By.XPATH, QUESTION_3)
        time.sleep(1)
        question_1.send_keys(new_address)
        time.sleep(1)
        question_2.send_keys(i_price)
        time.sleep(1)
        question_3.send_keys(i_link)
        time.sleep(1)
        submit = driver.find_element(By.XPATH, SUBMIT).click()
        time.sleep(1)
        driver.close()
    except FileExistsError:
        pass





