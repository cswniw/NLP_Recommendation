import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from scipy.io import mmwrite, mmread
import pickle
from gensim.models import Word2Vec

# 관계가 있다 없다는 cosin 값을 본다. 코싸인 값이 1이면 완전 같다. 1(0도), 0(90도), -1(180도)
# 코사인 직각 삼각형의 90도의 대변 t 밑변 x 사이 각 세타 / 코사인-세타 : x/t
def getRecommendation(cosine_sim) :
    simScore = list(enumerate(cosine_sim[-1]))    # 리스트로 묶여있으니 0이나 -1이나 같다.
    # sorted 전에 영화에 인덱스를 주자.
    simScore = sorted(simScore, key=lambda x : x[1], reverse=True)  # 내림차순 정리
    simScore = simScore[1:11]  # 0번은 자기 자신이니까 제외. 유사도 1이므로.
    movieidx = [i[0] for i in simScore]   # i[0]는 영화의 인덱스 // 유사한 10개 영화의 인덱스 받음.
    recMovieList = df_reviews.iloc[movieidx]
    return  recMovieList


df_reviews = pd.read_csv('./crawling_data/cleaned_review_2015_2021.csv')
Tfidf_matrics = mmread('./models/Tfidf_movie_review.mtx').tocsr()
with open('./models/tfidf.pickle', 'rb') as f:
    Tfidf = pickle.load(f)

################################################################################################
### 영화 제목을 키워드로 유사한 영화 찾기 / index를 이용

movie_name = '어벤져스: 엔드게임 (Avengers: Endgame)'
movie_idx = df_reviews[df_reviews['titles']== movie_name].index[0]
print(movie_idx)
# 예시. movie_idx = 10

print(df_reviews.iloc[movie_idx, 0])

cosine_sim = linear_kernel(Tfidf_matrics[movie_idx],
                           Tfidf_matrics)
# 좌표를 인자로 준다. // ex) 트랜짓 좌표와 나머지 모든 영화 좌표와의 cosine
# print(cosine_sim)    # [[0.05461841 0.05491788 0.05808229 ... 0.09792725 0.02666848 0.03823081]]
# print(len(cosine_sim[0]))    # 4191개의 영화

recommendation = getRecommendation(cosine_sim)
print(recommendation.iloc[:,0])
###############################################################################################

###############################################################################################
## 키워드로 검색
embedding_model = Word2Vec.load('./models/word2VecModel_2015_2021.model')
key_word = '토르'
sentence = [key_word] * 10   # 토르가 10번 들어있는 리스트
sim_word = embedding_model.wv.most_similar(key_word, topn=10)  # sim_word에 리스트로 받음.

words = []
for word, _ in sim_word :   # word는 단어 / _ 는 유사도
    words.append(word)
print(words)

for i, word in enumerate(words) :
    sentence += [word]*(10-i)        # 토르 10번 라그나로크 9번 갤럭시8번

sentence = ' '.join(sentence)
print(sentence)

sentence_vec = Tfidf.transform([sentence])
cosine_sim = linear_kernel(sentence_vec, Tfidf_matrics)
recommendation = getRecommendation(cosine_sim)
print(recommendation['titles'])
################################################################################################


############################ 줄거리나 리뷰로 검색 #################################
sentence = '어느 날 기이한 존재로부터 지옥행을 선고받은 사람들. ' \
           '충격과 두려움에 휩싸인 도시에 대혼란의 시대가 도래한다. 신의 심판을 외치며 세를 확장하려는 종교단체와 진실을 파헤치는 자들의 이야기.'
sentence_vec = Tfidf.transform([sentence])
cosine_sim = linear_kernel(sentence_vec, Tfidf_matrics)
recommendation = getRecommendation(cosine_sim)
print(recommendation['titles'])





