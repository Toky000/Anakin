from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import json
from bs4 import BeautifulSoup

sleepTimes = [2.1, 2.8, 3.2]

s = Service('D:/Projects/anakin_scraping-master/chromedriver.exe')
driver = webdriver.Chrome(service=s)
driver.implicitly_wait(5)
burl = "https://food.grab.com/sg/en/"
driver.get(url=burl)
driver.maximize_window()

my_location = WebDriverWait(driver, timeout=10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div[3]/div[2]/div/div[2]/div[1]/div/div/ul/li/div/span[1]/input")))
my_location.send_keys("Plaza Singapura" + Keys.ENTER)
driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[3]/div[2]/div/button").click()

uurl = "https://food.grab.com/sq/en/restaurants"

driver.get(uurl)
submit = driver.page_source
ld = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[3]/div[4]/div/div/div[4]/div/button")
ld.click()

counter = 0

while counter < 2:
    try:
        time.sleep(10)
        driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[3]/div[4]/div/div/div[4]/div/button")
        ld.click()
        counter += 1
    except:
        break

print("Counter quantity : " + str(counter))

time.sleep(9)
submitt = driver.page_source
src = BeautifulSoup(submitt, "html.parser").select("div.ant-row-flex.RestaurantListRow___1SbZY")

urls = []
burl = "https://food.grab.com"

for s in src:
    urs = s.findAll('a')
    urls = list(map(lambda x: burl + x.get("href"), urs))

print(urls)
print("\n".join(urls))

for url in urls:
    driver.get(url)
    src = driver.page_source
    soup = BeautifulSoup(src, "html.parser")
    entities = soup.find("script", type="application/json")
    try:
        info = json.loads(entities.text)
        vs = info["props"]["initialReduxState"]["pageRestaurantDetail"]["entities"]
    except:
        pass
    for key,value in vs.items():
        print(vs[key]['latlng'])
