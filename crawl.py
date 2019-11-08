from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options  

import os
from tqdm import tqdm 
import time 
import sys 
import csv

chrome_options = Options()  
chrome_options.add_argument("--headless") 
driver = webdriver.Chrome(os.path.abspath('/home/trungdunghoang/chromedriver'), chrome_options=chrome_options)

keyword = input("Query:")
url='https://publons.com/publon/?title={}&asjc=62'.format(keyword.replace(" ","%20"))
driver.get(url)

n_results = driver.find_element_by_xpath('//div[@class="number-text"]')
n_results = int(n_results.text.split(" ")[0])
print(n_results)

results = driver.find_elements_by_xpath('//div[@class="flex-row"]')
while(len(results)<n_results):
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(1)
    results = driver.find_elements_by_xpath('//div[@class="flex-row"]')

    print(len(results))

with open(os.path.join('output', keyword.replace(' ','_')+'.csv'), 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['Date', 'Title', 'PaperLink', 'Journal/Conference', 'JournalLink','Citations', 'Score'])
    for result in results[1:]:
        elems = result.find_elements_by_xpath("./*")
        row = [elems[0].text, elems[1].text, elems[1].get_attribute('href'), \
            elems[2].get_attribute('title'), elems[2].get_attribute('href')]
        try:
            row.append(int(elems[3].text))
        except:
            row.append(-1)

        try:
            row.append(int(elems[3].text))
        except:
            row.append(-1)
        writer.writerow(row)

f.close()           
driver.close()
