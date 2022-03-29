import pandas as pd
import glob

data_paths = glob.glob('./crawling_data/naverblog_raw_crawling_data/naver_reviews_*.csv')

df = pd.DataFrame()
for data_path in data_paths:
    df_temp = pd.read_csv(data_path)
    df_temp.columns = ['area', 'content', 'reviews']
    df = pd.concat([df, df_temp], ignore_index=True)

df.dropna(inplace=True)
df.drop_duplicates(inplace=True)
df.info()

df.to_csv('./crawling_data/naverblog_processed_crawling_data/naverblog_onesentence_reviews.csv', index=False)
