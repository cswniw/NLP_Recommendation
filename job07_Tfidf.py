# tf*idf 를 이용해 문장 유사도를 찾다 . term frequency

# https://class101.dev/ko/blog/2019/07/16/esmond/

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.io import mmwrite, mmread
import pickle

df_reviews = pd.read_csv('./crawling_data/cleaned_reviews_trip_naver.csv')
df_reviews.info()

Tfidf= TfidfVectorizer(sublinear_tf=True)
Tfidf_matrix = Tfidf.fit_transform(df_reviews['cleaned_sentences'])

with open('./models/tfidf.pickle', 'wb') as f :
    pickle.dump(Tfidf, f)

mmwrite('./models/Tfidf_attraction_review.mtx', Tfidf_matrix)

