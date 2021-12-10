from selenium import webdriver
import time
import pandas as pd

# 크롬 웹브라우저 실행
options = webdriver.ChromeOptions()
options.add_argument('lang=ko_KR')
options.add_argument('disable_gpu')
driver = webdriver.Chrome('./chromedriver', options=options)

df_reviews = pd.read_csv('./crawling_data/reviews_all.csv')
area = df_reviews['area'].tolist()
content = df_reviews['content'].tolist()
area_list = []
content_list = []
reviews_list = []

### 필히 경로 수정하고 저장명 확인 ######

for i in range(len(content)):
    url_list = []
    for j in range(1, 6):  # 블로그 페이지
        # url = 'https://section.blog.naver.com/Search/Post.naver?pageNo={}&rangeType=MONTH&orderBy=sim&startDate=2020-01-10&endDate=2021-12-10&keyword={}'.format(j, content[i])
        url = 'https://section.blog.naver.com/Search/Post.nhn?pageNo={}&rangeType=ALL&orderBy=sim&keyword={}'.format(
            j, content[i])
        driver.get(url)
        time.sleep(0.5)
        for k in range(1, 8):  # 각 블로그 주소 저장
            try:
                title_xpath = '/html/body/ui-view/div/main/div/div/section/div[2]/div[{}]/div/div[1]/div[1]/a[1]'.format(
                    k)
                title = driver.find_element_by_xpath(title_xpath).get_attribute('href')
                url_list.append(title)
            except:
                break

    reviews = ''
    for url in url_list:
        driver.get(url)
        driver.switch_to.frame('mainFrame')
        overlays = ".se-component.se-text.se-l-default"  # 내용 크롤링
        review = driver.find_elements_by_css_selector(overlays)
        review2 = driver.find_elements_by_css_selector('.post-view')
        review = review + review2
        for r in review:
            r = r.text.replace('\n', ' ')
            reviews = reviews + r
    print(content[i], reviews)
    area_list.append(area[i])
    content_list.append(content[i])
    reviews_list.append(reviews)

    if (i+1) % 10 == 0:
        df_review = pd.DataFrame({'area': area_list, 'content': content_list, 'reviews': reviews_list})
        print(df_review)
        df_review.to_csv('./crawling_data/naver/reviews_naver_{}_{}.csv'.format(i-9, i), index=False)
        area_list = []
        content_list = []
        reviews_list = []

df_review = pd.DataFrame({'area': area_list, 'content': content_list, 'reviews': reviews_list})
print(df_review)
df_review.to_csv('./crawling_data/naver/reviews_naver_remain.csv', index=False)
driver.close()
