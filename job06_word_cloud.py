import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import collections
from konlpy.tag import Okt
from matplotlib import font_manager, rc
import matplotlib as mpl
import numpy as np


font_path = './malgun.ttf'
font_name = font_manager.FontProperties(
    fname=font_path, size=8).get_name()
mpl.rcParams['axes.unicode_minus'] = False
rc('font', family=font_name)


df = pd.read_csv('./crawling_data/cleaned_reviews_trip_naver.csv')
print(df.head())

words = df[df['content'] == '모래시계 공원(강원도)']['cleaned_sentences']
# print(type(words))
# print(words)
# words = words[0].split()
words = words.iloc[0].split()
# print(words)    # 형태소들이 들어있는 하나의 리스트가 된다.


worddict = collections.Counter(words)  # 리스트 안의 요소의 빈도수를 세서 알려준다.
worddict = dict(worddict)
print(worddict)
wordcloud_img = WordCloud(
    background_color = 'white', max_words = 2000, font_path = font_path
).generate_from_frequencies(worddict)
plt.figure(figsize=(12, 12))
plt.imshow(wordcloud_img, interpolation='bilinear')
plt.axis('off')
plt.show()

#
# stopwords = ['영화', '감독', '개봉', '개봉일', '촬영',
#              '관객', '관람', '주인공', '출연', '배우',
#              '들이다', '푸다', '리뷰', '네이버']

exit()
from PIL import Image
alice_mask = np.array(Image.open('./bin_mask.jpg'))

wordcloud_img = WordCloud(
    background_color='white', max_words=2000, font_path=font_path,
    collocations=False, stopwords=stopwords, mask=alice_mask
).generate(df.cleaned_sentences[0])  # 문장 자체를 넣자.
plt.figure(figsize=(12, 12))
plt.imshow(wordcloud_img, interpolation='bilinear')
plt.axis('off')
# plt.show()