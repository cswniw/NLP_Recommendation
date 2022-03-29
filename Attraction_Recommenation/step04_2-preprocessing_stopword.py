import pandas as pd

df = pd.read_excel('crawling_data/cleaned_merged_reviews_trip_naver.xlsx', index_col=0)


##########     새로이 추가한 Stopword    #########

add_stopwords = pd.read_csv('./crawling_data/add_stopwords.csv', index_col=0)
add_stopwords = list(add_stopwords['add_stopword'])
# stopwords_add로 불용어를 추가한다.

count = 0
cleaned_sentences = []
for sentence in df['cleaned_sentences']:
    count += 1
    if count % 10 == 0:
        print('.', end='')
    if count % 100 == 0:
        print()

    words = []
    sentence = sentence.split()
    for word in sentence :
        if word not in add_stopwords :
            words.append(word)
    # 리스트를 다시 str 한줄로...
    cleaned_sentence = ' '.join(words)
    cleaned_sentences.append(cleaned_sentence)

df['cleaned_sentences'] = cleaned_sentences
print(df.head())
df = df[['area', 'content', 'cleaned_sentences']]
df.sort_values(by=['area','content'], axis=0, inplace=True)
df.info()

print(df.head())
df.to_csv('./crawling_data/drop_cleaned_merged_reviews_trip_naver.csv', index=False)


