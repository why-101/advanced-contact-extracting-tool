import csv
import itertools
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.by import By
import html2text
import re

# making list from CSV file
with open('CTRI.csv', 'r') as f:
    reader = csv.reader(f)
    your_list = list(reader)
j = list(itertools.chain.from_iterable(your_list))
res_lis = j[1:]
print(res_lis)

# defining web driver for chrome
s = Service('C:/Users/chait/Dropbox/PC/Downloads/chromedriver_win32 (1)/chromedriver.exe')
driver = webdriver.Chrome(service=s)

count = len(res_lis)

for company in res_lis:
    # searching on Google
    company = company.replace(' ', '+')
    driver.get('https:www.google.com/search?q=' + company)
    driver.find_element(By.XPATH, "//div[@class='g']//div[@class='yuRUbf']").click()

    # reading and downloading all the content from page
    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")

    # making list of elements from above
    list_1 = []
    for a in soup.findAll('a', href=True):
        c = (a['href'])
        ls = c
        list_1.append(str(ls))

    elem = driver.find_element(By.XPATH, "//*")
    source_code = elem.get_attribute("innerHTML")
    h = html2text.HTML2Text()
    h.ignore_links = True
    h.ignore_images = True
    h.ignore_tables = True
    h.ignore_emphasis = True
    r = h.handle(source_code)
    r = h.handle(source_code)
    rm = r.replace("\n", " ")
    list_2 = rm.split(" ")

    main_list = list_1+list_2
    result = []
    char = ['@', '91']

    for i in main_list:
        for j in char:
            if re.search(j, i):
                if len(i) < 100:
                    result.append(i)
    mails = [company, "-->"]
    for email in result:
        if re.match(r'[\w.-]+@[\w.-]+.\w+', email):
            mails.append(email)
    print(mails)

    time.sleep(1)
driver.close()