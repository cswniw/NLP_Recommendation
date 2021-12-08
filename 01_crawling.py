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
    reviews_list = []
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

            reviews = driver.find_element_by_class_name('mt10 hover-pointer').text
            reviews_list.append(reviews)
            print(reviews)

            for k in range(5) :
                driver.find_element_by_class_name('btn-next').send_keys(Keys.ENTER)
                reviews = driver.find_element_by_id('mt10 hover-pointer').text
                reviews_list.append(reviews)
                print(reviews)
                print(k)

            driver.back()
        except :
            print('except')
            time.sleep(1)
            driver.find_element_by_xpath(content_title_xpath).click()
            attraction = driver.find_element_by_xpath(attraction_xpath).text
            attraction_list.append(attraction)
            area = driver.find_element_by_xpath(area_xpath).text
            area_list.append(area)
            print(attraction, area)
            driver.back()

#
# //*[@id="reviews"]/div/div/div/div[3]/div[2]/ul/div[1]/li/div[2]/div[2]/a/p
# //*[@id="reviews"]/div/div/div/div[3]/div[2]/ul/div[2]/li/div[2]/div[2]/a/p
# //*[@id="reviews"]/div/div/div/div[3]/div[2]/ul/div[4]/li/div[2]/div[2]/a/p
# //*[@id="reviews"]/div/div/div/div[3]/div[2]/ul/div[6]/li/div[2]/div[2]/a/p
#
#
#

# <p class="mt10 hover-pointer ">명동 대림동 차이나타운 둘 다 유명한 명소..환전하러 명동 나갔다가 장마라서 비가 엄청 내렸지만 비오는 명동도 엄청 운치 있었어요~^^ 이젠 비도 그치고 서울 근교나 휴가 때 갈 명소를 트립 어플 찾는 중이네요ㅎ</p>















