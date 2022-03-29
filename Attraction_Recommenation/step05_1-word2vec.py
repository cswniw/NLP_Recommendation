# 단어를 벡터라이징화 하는 작업.
# 아나콘다에서 gensim 설치.
import pandas as pd
from gensim.models import Word2Vec

# 형태소들의 묶음(순서도 없는) bow 를 Word2Vec 모델에 준다.
# 단어의 수 만큼 차원이 생긴다.

review_word = pd.read_csv('./crawling_data/drop_cleaned_merged_reviews_trip_naver.csv')
review_word.info()

cleaned_token_review = list(review_word['cleaned_sentences'])
# print(len(cleaned_token_review)) ## 903개
# print(cleaned_token_review)
# 연꽃 시원하다 풍경 하루 힐링 해보다 어떻다 당일치기

cleaned_tokens = []
for sentence in cleaned_token_review :
    token = sentence.split()
    cleaned_tokens.append(token) # 이렇게 하면 2차원됨.
    # cleaned_tokens = cleaned_tokens + token

# print(cleaned_tokens)
# ex)'연등', '국내', '최대', '청동', '대불', '배경',
# print(len(cleaned_tokens))
# 903개 리스트 안에 리스트 형태로 903개


embedding_model = Word2Vec(cleaned_tokens, vector_size=100,
                           window=4, min_count=20, workers=6, epochs=100, sg=1)

# gensim 4.0.1 버젼
# 버젼에 따라 vecter_size -> size , epochs -> iter 로 바꿔야 한다. gensim 3.8.3
# http://doc.mindscale.kr/km/unstructured/11.html
# 학습 뒤 embedding_model로 리턴.
# 원래는 단어 사이즈 만큼 vector_size를 주나. 차원의 저주 유의로 100차원으로 줄이자
# workers 는 각자의 컴퓨터 cpu 사양에 맞춰 주어라. 작업관리자 > 성능 > CPU > 코어 확인
# window는 모델 학습 시킬 때 ex) 형태소 10의 문장이 있다면 4문장 단위로 학습.1~4, 2~5, 3~6 단위로 학습.
# min_count 는 전체 형태소의 데이타에서 20개 미만의 빈도로 나오는 단어는 거른다.

# 경고 문구 시 설치.
# conda install -c conda-forge python-levenshtein

embedding_model.save('./models/word2VecModel_attraction_reviews.model')

print(list(embedding_model.wv.index_to_key))
print(len(list(embedding_model.wv.index_to_key)))

# gensim 3.8 버젼에서는
# print(embedding_model.wv.vocab.keys())
# ex) ['좋다', '가다', '많다', '되어다', '오다', '사진', '먹다',
# print(len(embedding_model.wv.vocab.keys()))
# ex) 19910

# a = Word2Vec.load('./models/word2VecModel_2015_2021.model')
