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


df_reviews = pd.read_csv('./crawling_data/cleaned_reviews_trip_naver.csv')
Tfidf_matrics = mmread('./models/Tfidf_attraction_review.mtx').tocsr()
with open('./models/tfidf.pickle', 'rb') as f:
    Tfidf = pickle.load(f)

######################################## 영화 제목 / index를 이용 ########################################################
# movie_idx = df_reviews[df_reviews['content']=='명동(서울)'].index[0]
# print(movie_idx)
#
# # movie_idx = 10
# print(df_reviews.iloc[movie_idx, 0])
#
# cosine_sim = linear_kernel(Tfidf_matrics[movie_idx],
#                            Tfidf_matrics)
# # 좌표를 인자로 준다. // ex) 트랜짓 좌표와 나머지 모든 영화 좌표와의 cosine
# # print(cosine_sim)    # [[0.05461841 0.05491788 0.05808229 ... 0.09792725 0.02666848 0.03823081]]
# # print(len(cosine_sim[0]))    # 4191개의 영화
#
# recommendation = getRecommendation(cosine_sim)
# print(recommendation.iloc[:,0])
################################################################################################

################################################################################################
# ## 키워드로 검색
# embedding_model = Word2Vec.load('./models/word2VecModel_review.model')
# key_word = '겨울'
# sentence = [key_word] * 11   # 토르가 10번 들어있는 리스트
# sim_word = embedding_model.wv.most_similar(key_word, topn=10)  # sim_word에 리스트로 받음.
#
# words = []
# for word, _ in sim_word :   # word는 단어 / _ 는 유사도
#     words.append(word)
# print(words)
#
# for i, word in enumerate(words) :
#     sentence += [word]*(10-i)        # 토르 10번 라그나로크 9번 갤럭시8번
#
# sentence = ' '.join(sentence)
# print(sentence)
#
# sentence_vec = Tfidf.transform([sentence])
# cosine_sim = linear_kernel(sentence_vec, Tfidf_matrics)
# recommendation = getRecommendation(cosine_sim)
# print(recommendation['content'])
################################################################################################


############################ 줄거리나 리뷰로 검색 #################################
`# sentence = '겨울에 여자친구랑 여행가기 좋은곳 1박 2일 1박 2일로 여자친구랑 여행가기 좋은곳이 어디 있을까요? 뚜벅이고 경기도 광주 살고있는데 너무 막 먼곳은 힘들 거 같아요ㅠ 알려주세요!!'
# sentence_vec = Tfidf.transform([sentence])
# cosine_sim = linear_kernel(sentence_vec, Tfidf_matrics)
# recommendation = getRecommendation(cosine_sim)
# print(recommendation['content'])
`




