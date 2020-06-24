from collections import defaultdict
import sqlite3
import pandas as pd
import numpy as np
import surprise
from surprise import Reader, Dataset
from surprise.model_selection import KFold, cross_validate

def loaddata():
    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()
    # read table 
    df_store = pd.read_sql_query("SELECT * from api_store", con)
    df_review = pd.read_sql_query("SELECT * from api_storereview", con)
    # clonse DB connection
    con.close()
    stores = df_store[['id', 'store_name', 'category']]
    reviews = df_review[['user_id', 'store_id', 'total_score']]
    stores.rename(columns={'id': 'store_id'}, inplace=True)
    reviews.rename(columns={'total_score': 'rating'}, inplace=True)
    df = pd.merge(reviews, stores, on="store_id")
    return df

def validate(data):
    
    sim_options = {'name': 'pearson'}
    algo = surprise.KNNBasic(sim_options=sim_options)
    test_result = cross_validate(algo, data)
    return test_result['test_rmse'].mean()

def make_predictions(data):
    trainset = data.build_full_trainset()
    sim_options = {'name': 'pearson'}
    algo = surprise.KNNBasic(sim_options=sim_options)
    algo.fit(trainset)
    predictions = algo.test(trainset.build_testset())
    return predictions


def get_top_n(user_id, n=10):
    '''Return the top-N recommendation for each user from a set of predictions.

    Args:
        predictions(list of Prediction objects): The list of predictions, as
            returned by the test method of an algorithm.
        n(int): The number of recommendation to output for each user. Default
            is 10.

    Returns:
    A dict where keys are user (raw) ids and values are lists of tuples:
        [(raw item id, rating estimation), ...] of size n.
    '''
    df = loaddata()
    reader = Reader(rating_scale=(0.5, 5.0))
    data = Dataset.load_from_df(df[['user_id', 'store_id', 'rating']], reader)
    # print("KNN 모델 성능: ", validate(data))
    predictions = make_predictions(data)

    # First map the predictions to each user.
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, est))

    # Then sort the predictions for each user and retrieve the k highest ones.
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]

    # for uid, user_ratings in top_n.items():
    #     print(uid, [iid for (iid, _) in user_ratings])
    
    print(top_n)
    return top_n[user_id]

def main():
    top = get_top_n(68632, n=5)
    # print(top)
    # Print the recommended items for each user


if __name__ == "__main__":
    main()