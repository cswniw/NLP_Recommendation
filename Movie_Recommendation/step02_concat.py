import pandas as pd

# df = pd.read_csv('./crawling_data/2020/reviews_2020_2.csv')  #인덱스가 있으면 index_col = 0
# pprint.pprint(df)
# print(df.info())


### 수집한 데이터를 통합
df = pd.DataFrame()
for i in range(2015,2022) :
    df_temp = pd.read_csv('./crawling_data/reviews_{}.csv'.format(i))   #인덱스가 있으면 index_col = 0
    df_temp.dropna(inplace=True)   # 결측치 제거
    df_temp.drop_duplicates(inplace=True)   # 중복값 제거
    df_temp.columns = ['title','review']
    df_temp.to_csv('./crawling_data/reviews_drop_{}.csv'.format(i), index=False)
    df = pd.concat([df,df_temp], ignore_index=True)

df.drop_duplicates(inplace=True)
df.info()
df.to_csv('./crawling_data/naver_movie_reviews_2015_2021.csv', index=False)











