# Imports
import csv
import itertools
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.by import By
import html2text
import re
import random
from progress.bar import Bar

# Making list from CSV file

with open('your file', 'r') as f:
    reader = csv.reader(f)
    your_list = list(reader)

j = list(itertools.chain.from_iterable(your_list))  # Combining nested list as one
res_lis = j[1:]

print("whole list :", res_lis)  # Printing list
print(len(res_lis))

# Defining web driver for chrome
s = Service('your file path of chromedriver')
driver = webdriver.Chrome(service=s)

count = len(res_lis)  # Something that don't have to remove
have_to_find_manually = []  # find Manually

# Progress status bar
bar = Bar('Processing', max=20)

for company in res_lis:
    try:
        companies = company.replace(' ', '+')
        time.sleep(0.5)
        driver.get('https:www.google.com/search?q=' + companies)
        time.sleep(random.randrange(1, 3))
        driver.find_element(By.XPATH, "//div[@class='g']//div[@class='yuRUbf']").click()  # First result

        # Reading and downloading all the content from page
        content = driver.page_source
        soup = BeautifulSoup(content, features="html.parser")

        # Making list of elements from above Data
        list_1 = []
        for a in soup.findAll('a', href=True):
            c = (a['href'])
            ls = c
            list_1.append(str(ls))

        # Making list2 for below Data
        elem = driver.find_element(By.XPATH, "//*")
        source_code = elem.get_attribute("innerHTML")
        h = html2text.HTML2Text()
        h.ignore_links = True
        h.ignore_images = True
#        h.ignore_tables = True
        h.ignore_emphasis = True
        r = h.handle(source_code)
        rm = r.replace("\n", " ")
        list_2 = rm.split(" ")

        # Combining all the Data
        main_list = list_1 + list_2

        result = []
        char = ['@', '91', '2', 'mail']

        for i in main_list:
            for j in char:
                if re.search(j, i):
                    if (len(i) > 7) and (len(i) < 45):
                        result.append(i)


        def extract_string(lit):
            return [i for i in lit if len(i) <= 30]


        phon = []
        phones = extract_string(result)
        for i in phones:
            if re.search(r'\d{9}', i):
                phon.append(i)


        def remove_chars(list_of_strings, chars):
            return [string for string in list_of_strings if not any(char in string for char in chars)]

        phone = remove_chars(phon, ['N', 's', '#', '/','.'])

        # Picking up mails only
        mails = []
        for email in result:
            if re.match(r"[\w.-]+@[\w.-]+.\w+", email):
                mails.append(email)

        f_lit = mails + phone

        final_list = []
        for num in f_lit:
            if num not in final_list:
                final_list.append(num)

        final_things = {company: final_list}
        if len(final_list) > 0:
            print(final_things)
        else:
            have_to_find_manually.append(company)
        time.sleep(1)

    except:
        have_to_find_manually.append(company)
        pass
    bar.next()

bar.finish()
driver.close()
print("have_to_find_manually = ", have_to_find_manually)
print(len(have_to_find_manually))
