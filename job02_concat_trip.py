import pandas as pd
import glob

data_paths = glob.glob('./crawling_data/trip/reviews_{}.csv')
df = pd.DataFrame()
for data_path in data_paths:
    df_temp = pd.read_csv(data_path)
    df_temp.columns = ['area', 'content', 'reviews']
    df = pd.concat([df, df_temp], ignore_index=True)
df.dropna(inplace=True)
df.drop_duplicates(inplace=True)
df.sort_values(by=['area'], axis=0, inplace=True)
df.info()

area_list = []
content_list = []
one_sentences = []
for area in df['area'].unique():
    area_unique = df[df['area'] == area]
    for content in area_unique['content'].unique():
        temp = area_unique[area_unique['content'] == content]
        temp = temp['reviews']
        one_sentence = ' '.join(temp)
        stopwords_add = ['완벽해요', '최고에요', '좋아요', '보통이에요', '최악이에요', '작성일', '원문보기']
        for word in stopwords_add:
            one_sentence = one_sentence.replace(word, ' ')
        content = content + '(' + area + ')'

        area_list.append(area)
        content_list.append(content)
        one_sentences.append(one_sentence)


df_one_sentences = pd.DataFrame({'area': area_list, 'content': content_list, 'reviews': one_sentences})
df_one_sentences.info()
print(df_one_sentences.head())
df_one_sentences.to_csv('./crawling_data/reviews_1_3.csv', index=False)
