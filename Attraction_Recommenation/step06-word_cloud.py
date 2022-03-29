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


df = pd.read_csv('./crawling_data/drop_cleaned_merged_reviews_trip_naver.csv')
print(df.head())

content = '경복궁(서울)'
words = df[df['content'] == content]['cleaned_sentences']
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

exit()
######################################
stopwords = ['싶다']

from PIL import Image
alice_mask = np.array(Image.open('./travel_icon.png'))

wordcloud_img = WordCloud(
    background_color='white', max_words=2000, font_path=font_path,
    collocations=False, stopwords=stopwords, mask=alice_mask
).generate_from_frequencies(worddict)  # 문장 자체를 넣자.

plt.figure(figsize=(12, 12))
plt.imshow(wordcloud_img, interpolation='bilinear')
plt.axis('off')
plt.show()