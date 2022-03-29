import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from scipy.io import mmwrite, mmread
import pickle
from gensim.models import Word2Vec

# 관계가 있다 없다는 cosin 값을 본다. 코싸인 값이 1이면 완전 같다. 1(0도), 0(90도), -1(180도)
# 코사인 직각 삼각형의 90도의 대변 t 밑변 x 사이 각 세타 / 코사인-세타 : x/t

def getRecommendation(cosine_sim) :
    simScore = list(enumerate(cosine_sim[-1]))    # 리스트로 묶여있으니 0이나 -1이나 같다.
    # ex) [(0, 0.18777633855487236), (1, 0.22096990858660473),  .... (917, 0.15855474152191032), (918, 0.14953229333043086)]

    # sorted 전에 content에 인덱스를 주자.
    simScore = sorted(simScore, key=lambda x : x[1], reverse=True)  # 내림차순 정리
    simScore = simScore[1:11]  # 0번은 자기 자신이니까 제외. 유사도 1이므로.
    content_idx = [i[0] for i in simScore]   # i[0]는 Content의 인덱스 // 유사한 10개 영화의 인덱스 받음.
    recContentList = df_reviews.iloc[content_idx]
    return  recContentList



df_reviews = pd.read_csv('./crawling_data/drop_cleaned_merged_reviews_trip_naver.csv')
Tfidf_matrics = mmread('./models/Tfidf_attraction_review.mtx').tocsr()
with open('./models/tfidf.pickle', 'rb') as f:
    Tfidf = pickle.load(f)

######################################## 명소이름 / index를 이용 ########################################################

content_idx = df_reviews[df_reviews['content']=='명동(서울)'].index[0]
# print(content_idx)    # 명동 (서울) = 459
# exit()

# print(df_reviews.iloc[content_idx, 1])
# 2번째 인자에 0:지역(area) / 1:명소(content) / 2:리뷰(reviews) 이다.
cosine_sim = linear_kernel(Tfidf_matrics[content_idx],
                           Tfidf_matrics)
# 좌표를 인자로 준다. // ex) content 좌표와 나머지 모든 content 좌표와의 cosine
# print(cosine_sim)    # [[0.18777634 0.22096991 0.20372403 0.22204144 0.21083137 0.16709851....
# print(len(cosine_sim[0]))    # 919개의 명소


recommendation = getRecommendation(cosine_sim)
# print(recommendation)  # 상위 1개의 정보
# print(len(recommendation))   # getRecommendation 함수로 10개의 추천 명소 출력.
print(recommendation.iloc[:,1])   # 1은 명소(content) 컬럼 뜻함.

################################################################################################

################################################################################################
# ## 키워드로 검색
embedding_model = Word2Vec.load('./models/word2VecModel_attraction_reviews.model')
key_word = '벚꽃'
sentence = [key_word] * 11   # 토르가 10번 들어있는 리스트
sim_word = embedding_model.wv.most_similar(key_word, topn=10)  # sim_word에 리스트로 받음.

words = []
for word, _ in sim_word :   # word는 단어 / _ 는 유사도
    words.append(word)
print(words)
#
for i, word in enumerate(words) :
    sentence += [word]*(10-i)        # 토르 10번 라그나로크 9번 갤럭시8번
#
sentence = ' '.join(sentence)
print(sentence)
#
sentence_vec = Tfidf.transform([sentence])
cosine_sim = linear_kernel(sentence_vec, Tfidf_matrics)
recommendation = getRecommendation(cosine_sim)
print(recommendation['content'])
################################################################################################


############################ 줄거리나 리뷰로 검색 #################################
sentence = '겨울에 여자친구랑 여행가기 좋은곳 1박 2일 1박 2일로 외국인 여자친구랑 여행가기 좋은곳이 어디 있을까요? 뚜벅이고 경기도 살고있는데 너무 막 먼곳은 힘들 거 같아요ㅠ 알려주세요!!'
sentence_vec = Tfidf.transform([sentence])
cosine_sim = linear_kernel(sentence_vec, Tfidf_matrics)
recommendation = getRecommendation(cosine_sim)
print(recommendation['content'])




