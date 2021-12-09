from selenium import webdriver
import time
import pandas as pd

# 크롬 웹브라우저 실행
options = webdriver.ChromeOptions()
options.add_argument('lang=ko_KR')
options.add_argument('disable_gpu')
driver = webdriver.Chrome('./chromedriver', options=options)

df_reviews = pd.read_csv('./crawling_data/reviews_all.csv')   # 관광명소 이름 / 940개

area_list = df_reviews['area'].tolist()
area_list = area_list[0:236]
content_list = df_reviews['content'].tolist()
content_list = content_list[0:236]

# [0:236]  승우  [ 236 : 471] 지영   [471:706]   장일  [706:940]  은호

reviews_list = []

for i in range(len(content_list)):
    url_list = []
    for j in range(1, 6):  # 블로그 페이지
        url = 'https://section.blog.naver.com/Search/Post.nhn?pageNo={}&rangeType=ALL&orderBy=sim&keyword={}'.format(
            j, content_list[i])
        driver.get(url)
        time.sleep(0.5)

        for k in range(1, 8):  # 각 블로그 주소 저장
            title_xpath = '/html/body/ui-view/div/main/div/div/section/div[2]/div[{}]/div/div[1]/div[1]/a[1]'.format(k)
            title = driver.find_element_by_xpath(title_xpath).get_attribute('href')
            url_list.append(title)

    reviews = ''
    for url in url_list:
        driver.get(url)
        driver.switch_to.frame('mainFrame')
        overlays = ".se-component.se-text.se-l-default"  # 내용 크롤링
        review = driver.find_elements_by_css_selector(overlays)
        for r in review:
            r = r.text.replace('\n', ' ')
            reviews = reviews + r
    print(reviews)
    reviews_list.append(reviews)

    if (i+1) % 10 == 0:
        df_review = pd.DataFrame(
            {'area': area_list[i-9:i+1], 'content': content_list[i-9:i+1], 'reviews': reviews_list})
        print(df_review)
        df_review.drop_duplicates(inplace=True)
        df_review.to_csv('./crawling_data/crawling_data/naver/reviews_naver_{}_{}.csv'.format(i-9, i), index=False)
        reviews_list = []

driver.close()
