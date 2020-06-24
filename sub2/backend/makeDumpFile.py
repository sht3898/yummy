import schedule
import time
import pandas as pd
import surprise
import numpy as np
import os
import sqlite3

from sqlalchemy import create_engine
import pymysql

def makeDumpfile():
    # print('dump go')
    # # connect to DB
    # con = sqlite3.connect("db.sqlite3") # 모듈 호출시 사용경로
    # # print (os.getcwd()) #현재 디렉토리의
    # # con = sqlite3.connect("../db.sqlite3") # main용
    # cur = con.cursor()
    # # read table 
    # df_store = pd.read_sql_query("SELECT * from api_store", con)
    # df_review = pd.read_sql_query("SELECT * from api_storereview", con)

    # # clonse DB connection
    # con.close()
    db_connection_str = 'mysql+pymysql://hongju:hongju1004@i02b207.p.ssafy.io/yummy'
    db_connection = create_engine(db_connection_str)
    conn = db_connection.connect()
    df_store = pd.read_sql("SELECT * from api_store", con=conn)
    df_review = pd.read_sql("SELECT * from api_storereview", con=conn)
    conn.close()

    # select some columns
    stores = df_store[['id','store_name','category','addr']]
    reviews = df_review[['user_id','store_id','total_score']]

    # rename columns and return data
    reviews.rename(columns={'total_score':'rating'}, inplace=True)
    stores.rename(columns={'id':'store_id'},inplace=True)

    df = pd.merge(reviews, stores, on="store_id")
    # dump file 지정
    file_name = os.path.expanduser('dump_file')

    #swapping columns
    raw=df.loc[:,['user_id','store_id','rating']] 
    # when importing from a DF, you only need to specify the scale of the ratings.
    reader = surprise.Reader(rating_scale=(0,5)) 
    #into surprise:
    dataframe = surprise.Dataset.load_from_df(raw,reader)
    trainset = dataframe.build_full_trainset()
    algo = surprise.SVD()
    algo.fit(trainset)
    surprise.dump.dump(file_name, algo=algo)


if __name__ =='__main__':
    schedule.every(30).minutes.do(makeDumpfile)
    #update_log()
    while True:
        schedule.run_pending()
        time.sleep(1)