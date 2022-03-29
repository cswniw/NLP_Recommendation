import pandas as pd

### 동일 영화 대상의 리뷰들을 한 문단으로 합쳐준다.

df = pd.read_csv('./crawling_data/total/naver_movie_reviews_2015_2021.csv')

one_sentences = []

for title in df['title'].unique() :
    temp = df[df['title'] == title]
    temp = temp['review']
    one_sentence = ' '.join(temp)
    one_sentences.append(one_sentence)

df_one_sentences = pd.DataFrame(
    {'titles' : df['title'].unique(), 'reviews' : one_sentences})

print(df_one_sentences.head())
df_one_sentences.to_csv('./crawling_data/naver_movie_reviews_onesentence_2015_2021.csv',
                        index=False)



################################################################################################################
# df = pd.DataFrame({'title':['기생충', '기생충','기생충','강철비','강철비','기생충','강철비','강철비','강철비'],
#                    'reviews':['재밌다','재밌다','재미없다','멋있다','멋없다','재미없다','멋있다',
#                               '멋없다','멋있다']})
# print(df)
# print(df[df['title'] == '기생충'])
# print(df[df['title'] == '기생충']['reviews'])
# print(' '.join(df[df['title'] == '기생충']['reviews']))
################################################################################################################

