import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QStringListModel   # 이걸 linedit 에 적용하면 자동완성
from PyQt5 import uic
# pyrcc5 ./Asiae_AI_GUI/image/파일이름.qrc -o 파일이름.py

import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from gensim.models import Word2Vec
from scipy.io import mmread
import pickle

form_window = uic.loadUiType('./movie_recommendation.ui')[0]

class Exam(QWidget, form_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.df_reviews = pd.read_csv('./crawling_data/cleaned_review_2015_2021.csv')
        self.Tfidf_matrix = mmread('./models/Tfidf_movie_review.mtx').tocsr()
        self.embedding_model = Word2Vec.load('./models/word2VecModel_2015_2021.model')
        with open('./models/tfidf.pickle', 'rb') as f :
            self.Tfidf = pickle.load(f)

        self.titles = list(self.df_reviews['titles'])
        self.titles.sort()
        for title in self.titles :
            self.cmb_titles.addItem(title)


        model = QStringListModel()
        model.setStringList(self.titles)

        completer = QCompleter()
        completer.setModel(model)
        self.le_keyword.setCompleter(completer)


        self.cmb_titles.currentIndexChanged.connect(self.cmb_titles_slot)
        self.btn_recommend.clicked.connect(self.btn_recommend_slot)


    def cmb_titles_slot(self):   # 영화 디렉토리에서 찾아서 클릭 후 검색
        title = self.cmb_titles.currentText()
        recommendation_titles = self.recommend_by_movie_title(title)
        # movie_idx = self.df_reviews[self.df_reviews['titles'] == title].index[0]
        # cosine_sim = linear_kernel(self.Tfidf_matrix[movie_idx],
        #                            self.Tfidf_matrix)
        #
        # recommendation_titles = self.getRecommendation(cosine_sim)
        # recommendation_titles = '\n'.join(list(recommendation_titles))
        self.lbl_recommend.setText(recommendation_titles)

    def getRecommendation(self, cosine_sim):
        simScore = list(enumerate(cosine_sim[-1]))  # 리스트로 묶여있으니 0이나 -1이나 같다.
        # sorted 전에 영화에 인덱스를 주자.
        simScore = sorted(simScore, key=lambda x: x[1], reverse=True)  # 내림차순 정리
        simScore = simScore[1:11]  # 0번은 자기 자신이니까 제외. 유사도 1이므로.
        movieidx = [i[0] for i in simScore]  # i[0]는 영화의 인덱스 // 유사한 10개 영화의 인덱스 받음.
        recMovieList = self.df_reviews.iloc[movieidx]
        return recMovieList.titles

    def btn_recommend_slot(self) :    # 키워드 입력 검색. 영화 철자가 중요.

        key_word = self.le_keyword.text()
        if key_word :
            if key_word in self.titles :
                recommendation_titles = self.recommend_by_movie_title(key_word)
                # movie_idx = self.df_reviews[self.df_reviews['titles'] == key_word].index[0]
                # cosine_sim = linear_kernel(self.Tfidf_matrix[movie_idx],
                #                            self.Tfidf_matrix)
                #
                # recommendation_titles = self.getRecommendation(cosine_sim)
                # recommendation_titles = '\n'.join(list(recommendation_titles))
                self.lbl_recommend.setText(recommendation_titles)

            else :
                key_word = key_word.split()
                # if len(key_word) > 20:
                #     key_word = key_word[:20] 입력 수 제한하고자 할 때의 코드
                if len(key_word) > 10 :    #입력수가 10개 이상일 때 문장으로 받아보자.
                    sentence = ' '.join(key_word)
                    recommendation_titles = self.recommend_by_sentence(sentence)
                    # sentence_vec = self.Tfidf.transform([sentence])
                    # cosine_sim = linear_kernel(sentence_vec, self.Tfidf_matrix)
                    # recommendation_titles = self.getRecommendation(cosine_sim)
                    # recommendation_titles = '\n'.join(list(recommendation_titles))
                    self.lbl_recommend.setText(recommendation_titles)
                else:
                    sentence = [key_word[0]] * 11   # 토르가 10번 들어있는 리스트

                    try :
                        sim_word = self.embedding_model.wv.most_similar(key_word[0], topn=10)  # sim_word에 리스트로 받음.
                    except :
                        self.lbl_recommend.setText('제가 모르는 단어에요.')
                        return
                    words = []
                    for word, _ in sim_word :   # word는 단어 / _ 는 유사도
                        words.append(word)

                    for i, word in enumerate(words) :
                        sentence += [word]*(10-i)        # 토르 10번 라그나로크 9번 갤럭시8번

                    sentence = ' '.join(sentence)
                    recommendation_titles = self.recommend_by_sentence(sentence)
                    # sentence_vec = self.Tfidf.transform([sentence])
                    # cosine_sim = linear_kernel(sentence_vec, self.Tfidf_matrix)
                    #
                    # recommendation_titles = self.getRecommendation(cosine_sim)
                    # recommendation_titles = '\n'.join(list(recommendation_titles))
                    self.lbl_recommend.setText(recommendation_titles)



    def recommend_by_movie_title(self, title):
        movie_idx = self.df_reviews[self.df_reviews['titles'] == title].index[0]
        cosine_sim = linear_kernel(self.Tfidf_matrix[movie_idx],
                                   self.Tfidf_matrix)

        recommendation_titles = self.getRecommendation(cosine_sim)
        recommendation_titles = '\n'.join(list(recommendation_titles))
        return recommendation_titles


    def recommend_by_sentence(self, sentence) :
        sentence_vec = self.Tfidf.transform([sentence])
        cosine_sim = linear_kernel(sentence_vec, self.Tfidf_matrix)
        recommendation_titles = self.getRecommendation(cosine_sim)
        recommendation_titles = '\n'.join(list(recommendation_titles))
        return recommendation_titles

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = Exam()
    mainWindow.show()
    sys.exit(app.exec_())


