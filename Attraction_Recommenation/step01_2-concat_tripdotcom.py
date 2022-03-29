import pandas as pd
import glob

# 앞서 저장된 100개의 파일을 1개의 파일로 합친다.

data_paths = glob.glob('./crawling_data/tripdotcom_raw_crawling_data/tripdotcom_reviews_*.csv')
# *는 폴더 내 'reviews_'이름을 가진 모든 csv 파일을 검색한다.
# glob.glob로 해당 파일의 경로들을 리스트로 만들어 리턴해준다.

df = pd.DataFrame()
# 각 파일의 데이터를 취합하기 위한 빈 데이터 프레임을 만든다.
for data_path in data_paths:
    # for 문으로 리스트 안의 '파일 경로' 요소들에 접근.
    df_temp = pd.read_csv(data_path)
    df_temp.columns = ['area', 'content', 'reviews']
    # 각 파일의 컬럼명을 다시 정의하여 그로 인한 concat 작업 에러를 사전에 방지한다.
    df = pd.concat([df, df_temp], ignore_index=True)
    # 통합 작업을 하고 각 파일의 인덱스 정보는 무시한다.

########### 예시 파일은 1~36페이지의 각 명소들의 리뷰데이터 모음 파일.   ############
# 35 * 10 * (리뷰페이지의 리뷰 데이터의 합)
# ex) 9765 non-null object

df.dropna(inplace=True)
# 결측값이 존재하는 행 전체 삭제한다. default : axis=0
df.drop_duplicates(inplace=True)
# 중복값을 제거한다. ex) 9282 non-null object
df.sort_values(by=['area'], axis=0, inplace=True)
# 'area' 기준으로 데이터프레임을 정렬한다.


##### 예제. df.head()  ##########################################################################
#      area   content                                            reviews
# 4687  강원도  제이드가든수목원  霜牧澄临 5/5완벽해요! 원문보기 그 해 봄 바람이 불고있는 주요 촬영 장소는 어져...
# 2307  강원도  설악산 국립공원  永不言弃XZH 5/5완벽해요! 원문보기 어서, 운동을 좋아하는 사람, 피를 뿌려라....
# 2308  강원도  설악산 국립공원  xiaoxiaoyun 4/5최고에요! 원문보기 팀 투어, 특별한 기능이 없습니다, ...
# 2309  강원도  설악산 국립공원  精准弹幕 4/5최고에요! 원문보기 그것은 나에게 매우 의미가있다. 내가 놀러 갈 때...
# 2310  강원도  설악산 국립공원  zhenqing0109 4/5최고에요! 원문보기 이 공원은 겨울에 갈 것을 권장하며...
################################################################################################

###### 동일 지역 이름 분류 아래...리뷰 데이터를 통합하자.  ######

area_list = []
content_list = []
one_sentences = []
for area in df['area'].unique():
    # ['강원도' '경기도' '경상남도' '경상북도' '광주' '대구' '대전' '부산' '서울' '울산' '인천' '전라남도' '전라북도' '제주도' '충청남도' '충청북도']
    # ex) 강원도
    area_unique = df[df['area'] == area]
    # ex) df = df[df['area'] == '강원도']

    for content in area_unique['content'].unique():
        temp = area_unique[area_unique['content'] == content]
        # ex) df = df[df['content'] == '설악산 국립공원']

        temp = temp['reviews']
        # 해당 지역 이름 / 해당 명소 / 모든 리뷰
        one_sentence = ' '.join(temp)
        # 해당 리뷰들의 1개의 행으로 붙여준다.

        ###### 불필요한 불용어 제거 ######
        stopwords_add = ['완벽해요', '최고에요', '좋아요', '보통이에요', '최악이에요', '작성일', '원문보기']
        for word in stopwords_add:
            one_sentence = one_sentence.replace(word, ' ')

        content = content + '(' + area + ')'
        # 좀 더 정확한 명소 정보를 제공하기 위해 명소 뒤에 지역 이름을 붙여서 재정의해줌.

        area_list.append(area)  # ex) 강원도
        content_list.append(content)   #) 설악산 국립공원
        one_sentences.append(one_sentence)   # 설악산 국립공원의 모든 리뷰 (일부 불용어 제거)


##### 트립 닷컴의 데이터__ 한 개의 명소 당 한 개의 리뷰로 정리됨.


df_one_sentences = pd.DataFrame({'area': area_list, 'content': content_list, 'reviews': one_sentences})
df_one_sentences.info()
# print(df_one_sentences.head())
# df_one_sentences.to_csv('./crawling_data/tripdotcom_processed_crawling_data/tripdotcome_onesentence_reviews.csv', index=False)


### 중복값 처리 후에 남은 명소들 중에 부적절한 명소가 있는지 직접 데이터를 확인하며 조사한다.

####### 크롤링 작업 후  중복 데이터 처리 작업을 거친다.

# 명소 띄어쓰기 제거
content_list = []
for content in df['content']:
    for area in df['area'].unique():
        content = content.replace('('+area+')', '')
    content = ''.join(content.split())
    content_list.append(content)
df_temp = pd.DataFrame({'area': df['area'], 'content': content_list, 'reviews': df['reviews']})
df_temp.info()

# 중복 값 합치기
idx_list = []
for content in content_list:
    if content_list.count(content) > 1:
        idx = df_temp[df_temp['content'] == content].index
        area = set(df.loc[idx]['area'].tolist())
        if len(area) == 1:
            idx_list = idx_list + idx.tolist()
idx_list = list(set(idx_list))
df_temp = df_temp.loc[idx_list]
df_temp.drop_duplicates(subset='content', inplace=True)
df_temp.info()


# 띄어쓰기 복구
df.drop(index=idx_list, axis=0, inplace=True)
df = pd.concat((df, df_temp), sort=True)
df.info()

# 저장
import xlsxwriter # 엑셀로 저장할 시 engine=xlsxwriter


df.to_csv('./crawling_data/tripdotcom_processed_crawling_data/drop_tripdotcom_onesentence_reviews.csv', index=False)
df.to_excel('./crawling_data/tripdotcom_processed_crawling_data/drop_tripdotcom_onesentence_reviews.xlsx', engine=xlsxwriter)

##################################################
# 수작업 ~ 전수조사
#              changryog  ~> 창룡문
#              광고성 .. 또는 부적절한 명소.
## 저장한 df의 csv 파일을 엑셀화한 뒤 명소를 일일이 체크한다.
# drop할 명소 이름 앞에 '$' 문자를 넣어 표시한 뒤 csv파일로 다시 저장한다.

df = pd.read_excel('crawling_data/tripdotcom_processed_crawling_data/drop_tripdotcom_onesentence_reviews.xlsx', index_col=0)
# df.info()

for content in df['content'] :
    if '$' in content :
        index1 = df[df['content'] == content].index
        df.drop(index1, inplace=True)
df.info()
df.to_csv('./crawling_data/final_drop_tripdotcom_onesentence_reviews.csv', index=False)
