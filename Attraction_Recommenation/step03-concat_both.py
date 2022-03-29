import pandas as pd

df_trip = pd.read_csv('./crawling_data/final_drop_tripdotcom_onesentence_reviews.csv')
df_naver = pd.read_csv('./crawling_data/naverblog_processed_crawling_data/naverblog_onesentence_reviews.csv')
content_all = df_trip['content'].tolist()

area_list = []
content_list = []
review_list = []


### 트립닷컴 기준 명소이름으로 네이버 블로그 리뷰를 검색했을 때  특정명소에 관한 네이버리뷰가 없을 시
### 처리를 위해 try,except문으로 코딩한다.
for content in content_all:
    try:
        area = df_trip[df_trip['content'] == content]['area'].tolist()[0]
        trip_review = df_trip[df_trip['content'] == content]['reviews'].tolist()[0]
        naver_review = df_naver[df_naver['content'] == content]['reviews'].tolist()[0]
        total_review = trip_review + naver_review
        print(area, content)

        area_list.append(area)
        content_list.append(content)
        review_list.append(total_review)

    except:   # 네이버 블로그 리뷰가 없을 경우.
        area = df_trip[df_trip['content'] == content]['area'].tolist()[0]
        trip_review = df_trip[df_trip['content'] == content]['reviews'].tolist()[0]
        total_review = trip_review
        print(area, content)

        area_list.append(area)
        content_list.append(content)
        review_list.append(total_review)
        print('no naver review')



df_concat = pd.DataFrame({'area': area_list, 'content': content_list, 'reviews': review_list})
df_concat.info()
print(df_concat.head())
df_concat.to_csv('./crawling_data/merged_reviews_trip_naver.csv', index=False)
