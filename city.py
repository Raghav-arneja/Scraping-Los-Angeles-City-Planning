import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time

urls = [
    'https://planning.lacity.org/pdiscaseinfo/search/encoded/MjIxMDAz0',
    'https://planning.lacity.org/pdiscaseinfo/search/encoded/MjE5ODU30'
]
dataframes = []
dictionary ={}

for url in range(len(urls)):

    driver = webdriver.Chrome('C:/Users/Raghav/Documents/web scrapping udemy beginners/practice-web-scraping/chromedriver.exe')
    driver.get(urls[url])
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    # time.sleep(10)
    results = driver.find_elements_by_xpath("//*[@class= 'body-content']//*[@class = 'ng-star-inserted']//*[@class = 'theCaseData']//*[@class = 'ng-star-inserted']//*[@class = 'rowData'] ")
    entitlement_result_title = driver.find_element_by_xpath("//*[@class= 'body-content']//*[@class = 'ng-star-inserted']//*[@class = 'theCaseData']//*[@class = 'ng-star-inserted']//*[@class = 'rowData ng-star-inserted']//*[@class = 'title'] ").text
    entitlement_result_data = driver.find_element_by_xpath("//*[@class= 'body-content']//*[@class = 'ng-star-inserted']//*[@class = 'theCaseData']//*[@class = 'ng-star-inserted']//*[@class = 'rowData ng-star-inserted']//*[@class = 'data'] ").text


    titles = []
    datas = []


    for i in range(len(results)) :
        if 0<=i<=13 or 15<=i<=17:
            title = results[i].find_element_by_class_name('title').text
            data = results[i].find_element_by_class_name('data').text
            # elements_dict[title] = [data]
            titles.append(title)
            datas.append(data)
        elif i == 14:
            headers = results[i].find_elements_by_tag_name('th')
            bodies = results[i].find_elements_by_tag_name('td')

            for th, tb in zip(headers,bodies):
                # elements_dict[th.text] = [tb.text]
                titles.append(th.text)
                datas.append(tb.text)
        elif i==18 :
            button = results[i].find_element_by_tag_name('button')
            button.click()
            time.sleep(5)
            cases_tag = driver.find_elements_by_xpath('//html/body/div/div/div[2]/dx-scroll-view/div[1]/div/div[1]/div[2]/dx-data-grid/div/div[6]/div/table/tbody/tr/td/div/a')
            cases = ''
            for i in range(len(cases_tag)):
                if i == 0:
                    cases = cases_tag[i].text
                else :
                    cases = cases + ', ' +cases_tag[i].text
            
            # elements_dict[button.text] = [cases]
            titles.append(button.text)
            datas.append(cases)
        else :
            link = results[i].text
            title = link.split(': ')[-2]
            data = link.split(': ')[-1]
            # elements_dict[title] = [data]
            titles.append(title)
            datas.append(data)

    # print(data)
    titles.insert(18, entitlement_result_title)
    datas.insert(18 , entitlement_result_data)

    for t, d in zip(titles,datas):
        if url ==0:
            dictionary[t] = [d]
        else:
            dictionary[t].append(d)

    # df = pd.DataFrame(np.array([datas]), columns = titles)
    # df.set_index(titles[0], inplace = True)
    # df.to_csv('city_plan.csv')
        
    driver.quit()
print(dictionary)
df = pd.DataFrame(dictionary)
key_list = list(dictionary)
df.set_index(key_list[0], inplace = True)
df.to_csv('city_plan.csv')




