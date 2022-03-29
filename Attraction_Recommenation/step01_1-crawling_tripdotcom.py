from selenium import webdriver
import pandas as pd
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import time
from selenium.webdriver.common.keys import Keys

##### 셀레늄 웹드라이버 옵션
options = webdriver.ChromeOptions()
options.add_argument('lang=ko_KR')
options.add_argument('disable_gpu')
driver = webdriver.Chrome('./chromedriver', options=options)


# 수집할 지역,명소,리뷰 데이터를 리스트에 추가하기 위해 빈 리스트를 만듦. 특정 구간마다 저장 후 리스트 초기화를 진행.
area_list = []   # area : 지역 이름
content_list = []   # content : 명소 이름
reviews_list = []   # reviews : 리뷰

# 트립닷컴 여행 사이트의 '트립가이드>아시아>대한민국>명소' 카테고리의 국내 명소'3280'개 중
# 추천이 많은 순으로 정렬한 뒤 나타나는 1000개의 명소에 대한 데이터를 수집함.

for i in range(1, 101):   # 트립닷컴 웹사이트는 해당 데이터를 100개의 제한된 페이지를 통해 제공함.

    url = 'https://kr.trip.com/travel-guide/city-100042/tourist-attractions/{}.html'.format(i)
    # 각 100개의 페이지의 주소는 제일 뒷쪽의 숫자만 변하므로 for 문 코드를 적용.
    driver.get(url)

    for j in range(1, 11):   # 각 페이지마다 10개의 관광지 데이터가 있음.

        content_title_xpath = '//*[@id="list"]/div[5]/div[{}]/a/div[2]/h3'.format(j)
        # 하나의 페이지의 명소들의 각각의 Xpath는 위와 같은 패턴을 보임. 1~10까지. 따라서 for 문 코드를 적용.
        content = driver.find_element_by_xpath(content_title_xpath).text
        # 해당 xpath의 text는 '명소 이름'만 있으므로 '.text'로 명소 이름을 추출하여 content 변수로 받아줌.

        try:   # 네트워크 지연 등의 이슈를 미연에 방지하기 위해 try문으로 명소의 데이터에 접근함.
            driver.find_element_by_xpath(content_title_xpath).click()

        except:  # 네트워크 지연이 될 경우 타임슬립을 0.5초 준다.
            time.sleep(0.5)
            driver.find_element_by_xpath(content_title_xpath).click()

        area = driver.find_element_by_xpath('//*[@id="__next"]/div[2]/div/div/div[2]/nav/div[5]/a').text
        # 지역 이름은 해당 명소 데이터에 접근하면 찾아볼 수 있다. 명소의 고유 웹페이지의 접근 시 페이지 상단에 카테고리화되어 표시되어 있고,
        # 그 중에서 광역시,도  단위로 지역을 분류하기 위해 해당 xpath의 지역 이름을 수집하기로 함.
        # 이 작업을 통해 행여 같은 이름을 가진 2개 이상의 명소에 대해 각 명소의 지역 정보를 제공하여 혼동을 방지하고, (ex.러브랜드)
        # 이 후 네이버 블로그에서 데이터 검색 시 구체적인 검색이 가능하며, (ex. 검색어 : 명동(서울))
        # 명소를 추천할 때 명소의 위치 정보를 제공할 수 있다.


        for k in range(1, 100): # 명소의 고유 웹페이지에는 그 안에 따로 리뷰를 모은 웹페이지들이 존재한다.
                                # 리뷰의 웹페이지들을 클릭하여 넘겨도 명소의 고유 웹페이지 주소는 변경되지 않는다.
                                # 최대 100개의 웹페이지가 존재하고, 'next'버튼으로 탐색할 것이므로 for 문에 100번 반복할 range(숫자)를 준다.

            time.sleep(0.2)
            review = driver.find_element_by_class_name("gl-poi-detail_comment-list").text
            # 리뷰의 1개 페이지에 존재하는 모든 리뷰 데이터를 크롤링한다.
            # 리뷰의 각 페이지에는 4개에서~10개까지 리뷰의 수가 제각기 다른다.
            # 빠른 데이터 수집작업을 위해 모든 리뷰 데이터를 크롤링하여 이후에 전처리하기로 한다.

            review = review.replace('\n', ' ')
            # 리뷰 데이터의 개행문자를 공백으로 바꿔준다.

            if review:
                # 각 페이지에 리뷰 데이터가 있다면 '지역 이름,명소 이름, 리뷰'를 각각의 리스트에 추가해준다.
                area_list.append(area)
                content_list.append(content)
                reviews_list.append(review)
                print(area, content, review)

            # 현재 페이지의 리뷰 데이터를 처리했으면 다음 페이지에 접근한다.
            try:
                driver.find_element_by_class_name("btn-next.disabled")
                print('no more review')
                break
                # 최대 100개의 리뷰 페이지가 존재하고, 각 명소마다 존재하는 페이지 숫자가 다르다.
                # 마지막 페이지의 next버튼의 class_name을 찾으면 더 이상 리뷰가 존재하지 않으므로
                # for k 문을 break 하여 다음 명소의 데이터에 접근한다.

            except:
                try:
                    driver.find_element_by_class_name("btn-next").send_keys(Keys.ENTER)
                except:
                    print('no more review')
                    break
                # 그것이 아니라면 next버튼을 통해 해당 명소의 리뷰 페이지를 접근하여 리뷰 데이터를 수집한다.
                # next 버튼을 찾지 못한다면 더 이상 수집할 리뷰가 없으므로 break 하며 for k 문깨서 다음 명소에 접근하자.

        driver.back()
        # 리뷰 데이터 수집이 끝났으면 driver를 뒤로가기 하여  10개의 명소가 나열된 웹페이지로 돌아간다.
        # 이로써 1개의 명소 데이터를 모았다.


    # for i 문에서 1개 페이지의 10개 명소의 리뷰 데이터 작업이 끝나면 데이터를 저장하자. 총 100개의 파일이 저장된다.
    df_review = pd.DataFrame({'area': area_list, 'content': content_list, 'reviews': reviews_list})
    df_review.drop_duplicates(inplace=True)
    # df_review 데이터 프레임 원본에 혹시 모를 중복값을 제거한다.
    df_review.to_csv('./crawling_data/tripdotcom_raw_crawling_data/tripdotcom_reviews_{}.csv'.format(i), index=False)
    # 저장. 그 과정 중 csv 저장 작업 시 불필요하게 생성될 인덱스를 False하여 저장한다.
    area_list = []
    content_list = []
    reviews_list = []
    # 저장 후 다음 for i 문의  명소 데이터를 모으기 위해 각각의 리스트를 초기화해준다.

# 100(i)개의 페이지에 각 10(j)개의 명소 : 총 1000개 명소의 데이터를 모은다.
driver.close()
