# pip install konlpy -
# pip install tweepy == 3.10.0
# - java 설치후 java -version 확인
# - Jpype파일 드래그해오기
# - pip install Jpype파일이름

import pandas as pd
from konlpy.tag import Okt
import re

stopwords = pd.read_csv('./crawling_data/stopwords.csv', index_col=0) # 인덱스가 있기 때문에 index=col 제로 줌.
stopwords_list = list(stopwords['stopword'])    # 불용어 제거
stopwords_movie = ['영화', '감독', '개봉', '개봉일', '촬영',
             '관객', '관람', '주인공', '출연', '배우',
             '들이다', '푸다', '리뷰', '네이버']
# 영화 리뷰 데이터에서 자주 등장하는 단어를 찾아내 불용어 사전에 추가한다.
stopwords = stopwords_list + stopwords_movie


df = pd.read_csv('./crawling_data/naver_movie_reviews_onesentence_2015_2021.csv')
# print(df.head())

okt = Okt()

# print(re.sub('[^가-힇]', ' ', df.loc[0, 'reviews']))

#######################################################################
# sentence = re.sub('[^가-힇 ]', ' ', df.loc[0, 'reviews'])
# print(sentence)
# token = okt.pos(sentence, stem=True)
# print(token)
#######################################################################

count = 0   # 토큰화가 오래걸리니 진행상황을 파악하기 위함.

cleaned_sentences = []  # 리뷰를 분류해서 동사 형용사 명사만 추출하여 리스트에 추가.
for sentence in df.reviews :   # df['reviews']
    count += 1
    if count % 10 == 0 :
        print('.', end='')
    if count % 100 == 0 :
        print()

    sentence = re.sub('[^가-힇 ]', '', sentence)  # 2번째 인자는 .. 뺀자리를 2번째인자로 채운다.
    token = okt.pos(sentence, stem=True)
    # pos로 형태소 분리하면서 품사까지 받자. stem=True로 어간의 원형으로 가져오자.
    # 토큰은 형태소와 품사의 리스트로 된다.
    df_token = pd.DataFrame(token, columns=['word','class'])
    df_cleaned_token = df_token[(df_token['class'] == 'Noun') |   # 명사
                                (df_token['class'] == 'Verb') |   # 동사
                                (df_token['class'] == 'Adjective')]   # 형용사

    words = []   # 추출 품사 + 불용어 사전에 통과된 문자데이터를 저장할 리스트.
    for word in df_cleaned_token['word'] :
        if len(word) > 1 :
            if word not in stopwords :
                words.append(word)
    cleaned_sentence = ' '.join(words)
    cleaned_sentences.append(cleaned_sentence)

df['cleaned_sentences'] = cleaned_sentences
print(df.head())
print(df.info())

df = df[['titles','cleaned_sentences']]  # 또는 df.drop('reviews', inplace=True, axis=1)
df.to_csv('./crawling_data/cleaned_review_2015_2021.csv')


exit()

############# 스탑워즈.. 리스트화 하지 않아서 제대로 걸러지지 않았을 경우에 쓴 코드 ##############
df2 = pd.read_csv('./crawling_data/not_cleaned_review_2015-2021.csv', index_col=0)
print(df2)
cleaned_sentences = []
for cleaned_sentence in df2.cleaned_sentences :
    cleaned_sentence_words = cleaned_sentence.split()
    words = []
    for word in cleaned_sentence_words :
        if word not in list(stopwords['stopword']) :
            words.append(word)
    cleaned_sentence = ' '.join(words)
    cleaned_sentences.append(cleaned_sentence)
df2['cleaned_sentences'] = cleaned_sentences
df2.to_csv('./crawling_data/cleaned_review_2015_2021.csv', index=False)

#################################################################################




