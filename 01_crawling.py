# https://github.com/cswniw/recommend_attraction

from selenium import webdriver
import pandas as pd
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import time
from selenium.webdriver.common.keys import Keys

options = webdriver.ChromeOptions()
options.add_argument('lang=ko_KR')
options.add_argument('disable_gpu')
driver = webdriver.Chrome('./chromedriver', options=options)


for i in range(1,101) :
    url = 'https://kr.trip.com/travel-guide/city-100042/tourist-attractions/{}.html'.format(i)
    driver.get(url)

    attraction_list = []
    area_list = []
    review_list = []
    for j in range(1,11) :
        content_title_xpath = '//*[@id="list"]/div[5]/div[{}]/a/div[2]/h3'.format(j)
        attraction_xpath = '//*[@id="poi.detail.overview"]/div/div[1]/h1'
        area_xpath = '//*[@id="__next"]/div[2]/div/div/div[2]/nav/div[5]/a'
        try :
            time.sleep(1)
            driver.find_element_by_xpath(content_title_xpath).click()

            attraction = driver.find_element_by_xpath(attraction_xpath).text
            attraction_list.append(attraction)

            area = driver.find_element_by_xpath(area_xpath).text
            area_list.append(area)

            print(attraction, area)
            driver.back()
        except :
            print('except')
            time.sleep(1)
            driver.find_element_by_xpath(content_title_xpath).click()
            attraction = driver.find_element_by_xpath(attraction_xpath).text
            attraction_list.append(attraction)
            print(attraction, area)
            driver.back()


# \<li class="number active">1</li>
#
# // *[ @ id = "reviews"] / div / div / div / div[3] / div[2] / div / div / div / ul / li[3]
# // *[ @ id = "reviews"] / div / div / div / div[3] / div[2] / div / div / div / ul / li[2]
# // *[ @ id = "reviews"] / div / div / div / div[3] / div[2] / div / div / div / ul / li[1]