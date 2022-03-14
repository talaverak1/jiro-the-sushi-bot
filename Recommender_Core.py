# -*- coding: utf-8 -*-
"""
Created on Sat May 15 11:16:58 2021

@author: kma5
"""

import pandas as pd
#import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from surprise import Reader, Dataset, SVD, model_selection
from surprise.model_selection import KFold
from surprise import KNNWithMeans
from surprise import BaselineOnly

#import our data
df = pd.read_csv('/Users/kma5/.conda/envs/Virtual_Assistant/sushi_stats_extended.csv')
df2 = pd.read_csv('/Users/kma5/.conda/envs/Virtual_Assistant/sushi_names_keywords.csv')


#check our data
#print(df.head(5))
#print(df2.head(5))

#POPULARITY FILTERING
#Let's find out which sushi is popular! 
#First, we determine the top three sushi's on people's list

a = df['most_liked'].mode()
b = df['second'].mode()
c = df['third'].mode()

a1 = df2.loc[df2['sushi_id']==a[0]]
b1 = df2.loc[df2['sushi_id']==b[0]]
c1 = df2.loc[df2['sushi_id']==c[0]]

#print ('The sushi that take the top 3 spots on the list are:', a1.iloc[0]['sushi_name']+', ', b1.iloc[0]['sushi_name']+', and ',  c1.iloc[0]['sushi_name'])
#print('')
#This isn't very useful since it only tells us two sushis
#Let's look for the most popular sushis in all the top 10

d = df2.nlargest(3, ['vote_count'])


#print ('Most popular sushis (most votes in top 10): ', d.iloc[0]['sushi_name'] ,'with ', d.iloc[0]['vote_count'], 'votes', ',', 
#       d.iloc[1]['sushi_name'] ,'with ', d.iloc[1]['vote_count'], 'votes', ', and',
#       d.iloc[2]['sushi_name'] ,'with ', d.iloc[2]['vote_count'], 'votes.',
#       )
#print('')
#We'll do a weighted vote count, where each position below first is discounted: 
# Weighted vote = most_liked votes*100 + second*.90+ third*.80... tenth*.10

e = df.apply(pd.Series.value_counts)

counts = df2['vote_count']

e = e.join(counts)

def weighted_vote(one, two, three, four, five, six, seven, eight, nine, ten, count):
    return (((one*1)+(two*.9)+(three*.8)+(four*.7)+(five*.6)+(six*.5)+(seven*.4)+(eight*.3)+(nine*.2)+(ten*.1))/count)

e['weighted_vote'] = e.apply(lambda row : weighted_vote((row['most_liked']), (row['second']), (row['third']), (row['fourth']),(row['fifth']),(row['sixth']),(row['seventh']),(row['eighth']),(row['ninth']),(row['tenth']), (row['vote_count'])), axis = 1)

#Now we can redo our popularity equation, but using the weighted/corrected ratings for sushi
e2= e.head(100)['weighted_vote']

e2 =df2.join(e2)
e2['weighted_vote'] = e2['weighted_vote'].shift(-1)

d2 = e2.nlargest(3, ['weighted_vote'])


#print ('Most popular sushis (weighted votes): ', d2.iloc[0]['sushi_name'] , ',', 
#       d2.iloc[1]['sushi_name'] , ', and',
#       d2.iloc[2]['sushi_name'] , '.'
#       )
#print('')
#There's a shakeup in the rankings and this likely better represents the preferences of those surveyed.

#pop= e2.sort_values('weighted_sum', ascending=False)

#plt.figure(figsize=(12,4))

#plt.barh(pop['sushi_name'].head(6),pop['weighted_vote'].head(6), align='center',
#        color='skyblue')
#plt.gca().invert_yaxis()
#plt.xlabel("Weighted Votes")
#plt.title("Popular Sushis")

#Content BASED FILTERING 

#Now we will create a system based on filtering descriptions


#df2 = df2.set_index('sushi_name')

tfidf = TfidfVectorizer(stop_words='english')

df2['sushi_description_keyword'] = df2['sushi_description_keyword'].fillna('')

tfidf_matrix = tfidf.fit_transform(df2['sushi_description_keyword'])

#print(tfidf_matrix.shape)

cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

indices = pd.Series(df2.index, index=df2['sushi_name']).drop_duplicates()


# Function that takes in sushi name as input and outputs most similar sushi
def get_recommendations(sushi_name, cosine_sim=cosine_sim):
    # Get the index of the sushi
    idx = indices[sushi_name]

    # Get the pairwsie similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar movies
    sim_scores = sim_scores[1:4]

    # Get the movie indices
    sushi_indices = [i[0] for i in sim_scores]

    # Return the top 10 most similar movies
    return df2['sushi_name'].iloc[sushi_indices]

#x = get_recommendations('egg')

#print(x)



#Collaborative Filtering 
#We need to flip the data a little, so we pretend that the ratings are out of 10. Best is 10/10 worst is 1/10. 

ratings = pd.read_csv('/Users/kma5/.conda/envs/Virtual_Assistant/ratings_by_user.csv')

reader = Reader(rating_scale=(1,10))
data = Dataset.load_from_df(ratings[['user_id', 'sushi_id', 'rating']], reader)
kf = KFold(n_splits=5)
kf.split(data)

svd = SVD() #Matrix Factorization-based Algorithm
evaluate = model_selection.cross_validate(svd, data, measures=['RMSE', 'MAE'], cv=5, verbose=False)


# The RMSE is between 2.5 and 2.9 with very little variation. This means that the predictions the algorithm will make are likely to be reliable to an exact degree. 
# That said, sushi is a fairly distinct food so variation is expected. We are aiming for a sushi to be in a person's top three so an RMSE or MAE less than that will work. 

knnalgo = KNNWithMeans() #Nearest Neighbors approach but takes means into account

basicalgo = BaselineOnly() #Algorithm predicting the baseline estimate for a user and item

trainset = data.build_full_trainset()
#print('')
#print('Baseline Predictor')
basicalgo.fit(trainset)
#print(svd.predict(61200, 2, 5))
#print('')
#print(svd.predict(65001, 2, 5))
#print('')

#print('SVD')
svd.fit(trainset)
#print(svd.predict(61200, 2, 5))
#print('')
#print(svd.predict(65001, 2, 5))
#print('')

#print('KNN')
knnalgo.fit(trainset)
#print(knnalgo.predict(61200, 2, 5))
#print('')
#print(knnalgo.predict(65001, 2, 5))

#Purely on the basis of the ratings, this will determine an estimate of what a user will rate a different sushi.
#New users can be added and users with no data can be used as well. 


