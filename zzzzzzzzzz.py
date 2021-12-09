# https://github.com/cswniw/recommend_attraction

import requests
from selenium import webdriver
import pandas as pd
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import time
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup


options = webdriver.ChromeOptions()
options.add_argument('lang=ko_KR')
options.add_argument('disable_gpu')
driver = webdriver.Chrome('./chromedriver', options=options)

# from selenium import webdriver
# import chromedriver_autoinstaller
# chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]  #크롬드라이버 버전 확인
# try:
#     driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe')
# except:
#     chromedriver_autoinstaller.install(True)
#     driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe')
# driver.implicitly_wait(10)



for i in range(1,101) :     ## 추천 명소의 웹 페이지 수 // 총 100개
    url = 'https://kr.trip.com/travel-guide/city-100042/tourist-attractions/{}.html'.format(i)
    driver.get(url)

    attraction_list = []
    area_list = []
    reviews_list = []

    print('i', i)
    for j in range(1,11) :   ## 페이지 하나 당 10개의 추천 명소
        content_title_xpath = '//*[@id="list"]/div[5]/div[{}]/a/div[2]'.format(j)
        # try :
        time.sleep(1)
        driver.find_element_by_xpath(content_title_xpath).click()  # 추천 명소 클릭
        time.sleep(1)
        # 지역과 관광명소 크롤링
        attraction_name_xpath = '//*[@id="poi.detail.overview"]/div/div[1]/h1'
        area_name_xpath = '//*[@id="__next"]/div[2]/div/div/div[2]/nav/div[5]/a'
        # 관광명소 명을 리스트에 추가
        attraction_name = driver.find_element_by_xpath(attraction_name_xpath).text
        attraction_list.append(attraction_name)
        # 지역 명을 리스트에 추가
        area_name = driver.find_element_by_xpath(area_name_xpath).text
        area_list.append(area_name)

        print(attraction_name, area_name)
        print('j', j)

        for k in range(1) :  # 관광 명소 내의 리뷰 페이지 숫자.
            print('k', k)
            for l in range(1, 10) :  # 리뷰 페이지 당 리뷰 갯수.
                print('l', l)
                try :
                    try :
                        time.sleep(1)
                        reviews_xpath = '//*[@id="reviews"]/div/div/div/div[2]/div[2]/ul/div[{}]/li/div[2]/div[2]/a/p'.format(l)
                        review = driver.find_element_by_xpath(reviews_xpath).text
                        print(review)

                    except NoSuchElementException :
                        time.sleep(1)
                        reviews_xpath = '//*[@id="reviews"]/div/div/div/div[3]/div[2]/ul/div[{}]/li/div[2]/div[2]/a/p'.format(l)
                        review = driver.find_element_by_xpath(reviews_xpath).text
                        print(review)
                        print('no_such', l)
                except :
                    print('no more reviews')
            time.sleep(1)
            try :
                driver.find_element_by_xpath('//*[@id="reviews"]/div/div/div/div[2]/div[2]/div/div/div/button[2]').send_keys(Keys.RETURN)
            except :
                driver.find_element_by_xpath('//*[@id="reviews"]/div/div/div/div[3]/div[2]/div/div/div/button[2]').send_keys(Keys.RETURN)

        # except:
        #     print('except')
        #     driver.get(url)

        # except:
        #     print('!')
                # for l in range(1,8) :
                #     try :
                #         time.sleep(1)
                #         print('1')
                #         # css_selecter = '#reviews > div > div > div > div.ContentContainer-tlt00z-0.bddgEJ > div.bgff.ovh > ul > div:nth-child(1) > li > div.gl-poi-detail_comment-content > div.burited_point > a > p'
                #         reviews_xpath = '//*[@id="reviews"]/div/div/div/div[3]/div[2]/ul/div[{}]/li/div[2]/div[2]/a/p'.format(l)
                #         reviews_id = '//*[@id="reviews"]/div/div/div/div[3]/div[2]/ul/div[{}]/li/div[2]/div[2]/a/p'.format(l)
                #         print('2')
                #         time.sleep(1)
                #
                #         # review = driver.find_element_by_css_selector(css_selecter)
                #         # review = driver.find_element_by_xpath(reviews_xpath)
                #         # review = driver.find_elements_by_class_name('mt10.hover-pointer').text
                #         # review_2 = driver.find_element_by_class_name('mt10.hover-pointer show-lines-review-text-5').text
                #         print(review)
                #         # print(review_2)
                #         print('l', l)






























