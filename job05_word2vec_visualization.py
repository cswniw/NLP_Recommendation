# 100차원이기에 2차원으로 축소하여 시각화하자.

import pandas as pd
import matplotlib.pyplot as plt
from gensim.models import Word2Vec
from sklearn.manifold import TSNE   # 차원 축소를 해줌.. 티쓰니
from matplotlib import font_manager, rc  # 한글 써야 하니 한글 폰트가 필요하다.
import matplotlib as mpl

font_path = './malgun.ttf'
font_name = font_manager.FontProperties(
    fname=font_path).get_name()
mpl.rcParams['axes.unicode_minus'] = False
rc('font', family=font_name)

embedding_model = Word2Vec.load('./models/word2VecModel_2015_2021.model')

key_word = '여름'
sim_word = embedding_model.wv.most_similar(key_word, topn=10)
print(sim_word)
# topn 키워드와 가장 가까이 배치된 단어 100개를 찾아줌(topN) / 벡터를 기준으로해서 가까운 단어들이 유사하다고 본다.


# 시각화를 위한 차원 축소 알고리즘 중 TSNE 를 써보자

vectors = []
labels = []
for label, _ in sim_word :     # ex) print(label, _) -->>  영화인 0.7705941200256348
    labels.append(label)
    vectors.append(embedding_model.wv[label])
    # 모델한테 단어를 주면 그 단어의 100차원 벡터를 줌.
    # 그럼 벡터스에는 100개의 좌표가 들어간다.

# print(vectors[0])
# print(len(vectors[0]))

df_vectors = pd.DataFrame(vectors)
print(df_vectors.head())

tsne_model = TSNE(
    perplexity=40, n_components=2, init='pca', n_iter=2500)  #  random_state=23

# knn  과   t_sne  설명.
#  https://gaussian37.github.io/ml-concept-t_sne/

# n_components  차원 수  //  random_state 랜덤값이지만 결과는 같은.
# perplexity = knn에서의 k 값  //  n_iter 에폭




new_value = tsne_model.fit_transform(df_vectors)   # new_value에는 2개의 벡터값이 들어간다.
df_xy = pd.DataFrame({'words':labels, 'x':new_value[:, 0], 'y':new_value[:,1]})
print(df_xy.head(10))
print(df_xy.shape)

df_xy.loc[df_xy.shape[0]] = (key_word, 0, 0)
# key_word를 기준으로 각 단어의 x,y 좌표를 알아보기 위해 0,0 좌표로 추가해줌.
print(df_xy.tail(11))  # 마지막 행에서 확인 가능.

plt.figure(figsize=(8,8))
plt.scatter(0, 0, s=1500, marker='*')  # 한 가운데 별 그려놓고.

for i in range(len(df_xy.x) - 1) :    # i는 0~100 까지 총 101
    a = df_xy.loc[[i, len(df_xy.x)-1], :]
    # i 와 맨 마지막 'key_word'까지 줄 긋겠다.
    # 유사단어 100개와 키워드 사이의 선 100개를 긋겠다.
    # key_word와 선을 긋기 위해 마지막 key_word 행의 인덱스 값을 줌.
    plt.plot(a.x, a.y, '-D', linewidth=2)
    plt.annotate(df_xy.words[i], xytext=(5,2), xy=(df_xy.x[i], df_xy.y[i]),
                 textcoords='offset points', ha='right', va='bottom')
    # annotate 그림 주석 다는 함수.
    # ha = horizontal
    # va = vertical
plt.show()



'''고지마 히로유키//
세상에서 가장 쉬운 통계학입문
세상에서 가장 쉬운 베이즈통계학입문

도 추천..  중1 수학 수준으로 통계학의 핵심만 알고 싶을 때.. 가볍게 읽기 좋습니다.'''