# import pandas as pd
#
# df_naver = pd.read_csv('./crawling_data/naver/semi_final_concat_reviews_naver_0_940.csv')
# df_trip = pd.read_csv('./crawling_data/total_reviews.csv')
#
# print(len(df_naver))
# print(len(df_trip))
# exit()
# df_naver['content']
#
#
# if df_naver['content'] == df_trip['content'] :
#     total_review = df_naver['reviews'] + df_trip['reviews']
#     df_both = pd.DataFrame({'content':df_naver['content'], 'reviews':total_review})
#
# print(df_both.head())


################################################
#
# import pandas as pd
#
# df_trip = pd.read_csv('./crawling_data/reviews_all.csv')
# df_naver = pd.read_csv('./crawling_data/naver/semi_final_concat_reviews_naver_0_940.csv')
#
# content_all = df_trip['content'].tolist()
#
# area_list = []
# content_list = []
# review_list = []
#
# for content in content_all:
#     try :
#         area = df_trip[df_trip['content'] == content]['area'][0]
#         trip_review = df_trip[df_trip['content'] == content]['reviews'][0]
#         naver_review = df_naver[df_naver['content'] == content]['reviews'][0]
#         total_review = trip_review + naver_review
#         # print(area, content, total_review)
#
#         area_list.append(area)
#         content_list.append(content)
#         review_list.append(total_review)
#     except:
#         area = df_trip[df_trip['content'] == content]['area'][0]
#         trip_review = df_trip[df_trip['content'] == content]['reviews'][0]
#         total_review = trip_review
#
#         area_list.append(area)
#         content_list.append(content)
#         review_list.append(total_review)
#
#
#
# df_concat = pd.DataFrame({'area': area_list, 'content': content_list, 'reviews': review_list})
# df_concat.info()
# print(df_concat.head())
# df_concat.to_csv('./crawling_data/reviews_trip_naver.csv', index=False)



import pandas as pd

df = pd.read_csv('./crawling_data/reviews_trip_naver.csv')
df.info()
exit()
#######################################################################
df_trip = pd.read_csv('./crawling_data/reviews_all.csv')
df_naver = pd.read_csv('./crawling_data/naver/semi_final_concat_reviews_naver_0_940.csv')

content_all = df_trip['content'].tolist()

area_list = []
content_list = []
review_list = []

for content in content_all:
    try:
        area = df_trip[df_trip['content'] == content]['area'].tolist()[0]
        trip_review = df_trip[df_trip['content'] == content]['reviews'].tolist()[0]
        naver_review = df_naver[df_naver['content'] == content]['reviews'].tolist()[0]
        total_review = trip_review + naver_review
        print(area, content)

        area_list.append(area)
        content_list.append(content)
        review_list.append(total_review)
    except:
        area = df_trip[df_trip['content'] == content]['area'].tolist()[0]
        trip_review = df_trip[df_trip['content'] == content]['reviews'].tolist()[0]
        # naver_review = df_naver[df_naver['content'] == content]['reviews'].tolist()[0]
        total_review = trip_review
        print(area, content)

        area_list.append(area)
        content_list.append(content)
        review_list.append(total_review)
        print('no naver review')



df_concat = pd.DataFrame({'area': area_list, 'content': content_list, 'reviews': review_list})
df_concat.info()
print(df_concat.head())
df_concat.to_csv('./crawling_data/reviews_trip_naver.csv', index=False)
