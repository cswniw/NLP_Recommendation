from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE
import xlsxwriter
from selenium import webdriver
import time
import pandas as pd

# 크롬 웹브라우저 실행
options = webdriver.ChromeOptions()
options.add_argument('lang=ko_KR')
options.add_argument('disable_gpu')
driver = webdriver.Chrome('./chromedriver', options=options)

#### 트립닷컴의 명소 중  영문 명소, 중복되는 명소, 광고성 짙은 명소, 부적절한 명소를 제거한
####   csv파일에서 명소 이름을 추출해서 네이버 블로그 검색창에 입력하여 블로그 리뷰 데이터를 수집함.

df_reviews = pd.read_csv('./crawling_data/final_drop_tripdotcom_onesentence_reviews.csv', index=False)
# 해당 csv파일 read.
area = df_reviews['area'].tolist()
# 지역 이름을 리스트로 나열.
content = df_reviews['content'].tolist()
# 명소 이름을 리스트로 나열.

area_list = []
content_list = []
reviews_list = []

for i in range(len(content)):   # 지역 명소의 이름으로 검색어 입력 즉, 명소의 숫자만큼 for i 문을 실행.
    url_list = []
    # 먼저 관련 블로그들의 url을 미리 추출한다.
    for j in range(1, 6):  # 블로그 검색 결과 5번째 페이지까지 노출된 블로그의 url을 수집함.
        url = 'https://section.blog.naver.com/Search/Post.nhn?pageNo={}&rangeType=ALL&orderBy=' \
              'sim&keyword={}'.format(j, content[i])  # content[i]로 인덱스하여 명소 이름을 입력한다.
        driver.get(url)
        time.sleep(0.5)

        for k in range(1, 8):  # 한 페이지당 노출되는 블로그의 수는 7개.
            try:
                title_xpath = '/html/body/ui-view/div/main/div/div/section/div[2]/div[{}]/' \
                              'div/div[1]/div[1]/a[1]'.format(k)
                # 나열된 블로그들의 xpath로 주소의 규칙을 위와 같이 발견.

                title = driver.find_element_by_xpath(title_xpath).get_attribute('href')
                url_list.append(title)
                # 각 블로그들의 url을 수집하여 저장한다.

            except:
                break
                # 검색된 블로그나 페이지 수가 모자르면 break로 나온다.


    # 위의 수집된 url을 방문하여 리뷰 text를 수집한다.
    reviews = ''
    for url in url_list:
        driver.get(url)
        driver.switch_to.frame('mainFrame')  # 네이버 블로그는 iframe이 적용되므로 driver가 이를 인식하게끔 해준다.
        overlays = ".se-component.se-text.se-l-default"  # 블로그 본문의 html 문장구조.

        review = driver.find_elements_by_css_selector(overlays)
        review2 = driver.find_elements_by_css_selector('.post-view')
        review = review + review2

        # 네이버 블로그의 버젼에 따라 본문 내용을 수집할수있는 html 구조가 다르므로
        # review / review2  의 2가지 방법으로 데이터를 수집한 뒤 병합한다.

        for r in review:
            r = r.text.replace('\n', ' ')
            reviews = reviews + r
        # 수집한 본문 내용에서 개행문자를 공백으로 바꿔준다.

    print(content[i], reviews)
    area_list.append(area[i])
    content_list.append(content[i])
    reviews_list.append(reviews)


    if (i+1) % 10 == 0:
        df_review = pd.DataFrame({'area': area_list, 'content': content_list, 'reviews': reviews_list})
        # print(df_review)
        df_review.to_csv('./crawling_data/naverblog_raw_crawling_data/naver_reviews_{}_{}.csv'.format(i-9, i), index=False)

        area_list = []
        content_list = []
        reviews_list = []

    # 10개의 명소에 관한 블로그 리뷰가 모일 때 마다 저장을 한뒤,
    # 뒤의 코드로 마지막 10개 미만의 명소의 블로그 리뷰 데이터를 저장할 코드를 작성한다.

    # if i == 126 :
    #     break

df_review = pd.DataFrame({'area': area_list, 'content': content_list, 'reviews': reviews_list})
print(df_review)
df_review.to_csv('./crawling_data/naverblog_raw_crawling_data/naver_reviews_remain.csv', index=False)
driver.close()
