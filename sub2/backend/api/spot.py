import json
import pickle
import sqlite3
import pandas as pd
import numpy as np
import sklearn
from sklearn.metrics.pairwise import cosine_similarity, linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer
from konlpy.tag import Okt

from sqlalchemy import create_engine
import pymysql

def loaddata():
    # con = sqlite3.connect("db.sqlite3")
    # cur = con.cursor()
    # # read table 
    # df_spot = pd.read_sql_query("SELECT * from api_spot", con)
    # # clonse DB connection
    # con.close()
    db_connection_str = 'mysql+pymysql://hongju:hongju1004@i02b207.p.ssafy.io/yummy'
    db_connection = create_engine(db_connection_str)
    conn = db_connection.connect()
    df_spot = pd.read_sql('SELECT * FROM api_spot', con=conn)
    conn.close()
    
    # spots에서 원하는 데이터만 추출
    pd.options.mode.chained_assignment = None
    spots = df_spot[['id', 'overview']]
    spots.rename(columns={'id':'spot_id'}, inplace=True)

    # overview에서 한글 키워드 추출
    okt = Okt()
    nouns = []
    for _, spot in spots.iterrows():
        temp = okt.nouns(spot['overview'])
        words = ''
        for t in temp:
            words += t + ' '
        nouns.append([spot['spot_id'], words[:-1]])

    # 키워드 데이터 프레임화
    nouns_frame = pd.DataFrame(nouns, columns=["spot_id", "description"])

    # 키워드 데이터프레임 저장
    nouns_frame.to_pickle('./spot.pkl')
    okt_frame = pd.read_pickle('./spot.pkl')

    # 벡터화 맟 tf-idf 연산
    tf = TfidfVectorizer(min_df=0)
    tfidf_matrix = tf.fit_transform(okt_frame['description'])
    cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

    results = {}
    for idx, row in okt_frame.iterrows():
        similar_indices = cosine_similarities[idx].argsort()[:-100:-1] 
        similar_items = [(cosine_similarities[idx][i], okt_frame['spot_id'][i]) for i in similar_indices] 
        results[row['spot_id']] = similar_items[1:]

    # 데이터 파일 저장
    with open('spot_result.pickle', 'wb') as f:
        pickle.dump(results, f)


def item(id):
    okt_frame = pd.read_pickle('./spot.pkl')
    return okt_frame.loc[okt_frame['spot_id'] == id]['spot_id'].to_string().split()[1]

# Just reads the results out of the dictionary.
# spot_id: 추천받고자 하는 장소 번호, num: 추천 받을 개수
def recommend(spot_id, num=3):
    with open('spot_result.pickle', 'rb') as f:
        results = pickle.load(f)
    print("Recommending " + str(num) + " products similar to " + item(spot_id) + "...")   
    print("-------")    
    recs = results[spot_id][:num]
    rec_list = []
    for rec in recs: 
        print("Recommended: " + item(rec[1]) + " (score:" +      str(rec[0]) + ")")
        rec_list.append(item(rec[1]))
    return rec_list

if __name__ == "__main__":
    recommend(spot_id=125266, num=5)
    
    '''
    사용예시
    
    recs = results[spot_id][:num]
    rec_list = []
    for rec in recs:
        print(' '.join(df_spot.loc[df_spot['id'] == int(rec)]['spot_name'].to_string().split()[1:]))
        rec_list.append(item(rec[1]))
    
    출력결과
    군위 장곡자연휴양림
    주천강자연휴양림
    국립횡성숲체원
    안동호반자연휴양림
    금강자연휴양림(금강수목원,산림박물관)
    '''
