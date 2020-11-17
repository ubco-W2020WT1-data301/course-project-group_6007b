import pandas as pd
import numpy as np
import datetime
import pandas_profiling
import seaborn as sns
import matplotlib.pylab as plt
import sys, os

def load_and_process (data):
    
    country = data
    df = pd.DataFrame()
    df1 = pd.DataFrame()

    for c in country:
        df1 = pd.read_csv('../../data/raw/'+ c +'_youtube_trending_data.csv',parse_dates= ['trending_date','publishedAt'])
        df1['country']= c
        df = pd.concat([df,df1])
    
        #change the datetime
    df["trending_date"] = df.apply(lambda row: pd.to_datetime(row["trending_date"]), axis=1)
    df["publishedAt"] = df.apply(lambda row: pd.to_datetime(row["publishedAt"]), axis=1)

        #category ID dictionary
    category_replace = {
              1:'Film & Animation',
              2:'Autos & Vehicles',
              10:'Music',
              15:'Pets & Animals',
              17:'Sports',
              19:'Travel & Events', 
              20:'Gaming',
              21:'Videoblogging',
              22: "People & Blogs",
              23: "Comedy", 
              24: "Entertainment",
              25: "News & Politics", 
              26: "Howto & Style", 
              27: "Education", 
              28: "Science & Technology",
              29: 'NaN'
        }

        #clean the dataset
    df_clean = (
            pd.DataFrame(data=df)
            .drop(columns = ['thumbnail_link','comments_disabled','ratings_disabled','description','title','channelId'])
            .replace({"categoryId":category_replace}).rename(columns= {'categoryId':'category'})
            .drop(df[df['categoryId']=='NaN'].index).sort_values('trending_date')
            .reset_index().drop(columns = ['index'])
    )
    
    #turn tags into actual list
    df_clean["tags"] = df_clean.apply(lambda row: row["tags"].split("|"), axis=1)
    
    #calculate the videos' like to dislike ratio (assuming that there are likes and dislikes)
    df_clean["ratio"] = df_clean.apply(lambda row: 0 if row["dislikes"]==0 else (row["likes"]/row["dislikes"]), axis=1)
    
    df_last = (
        pd.DataFrame(data=df_clean)
        .drop_duplicates(['video_id'], keep='last')
        .drop(df_clean[df_clean['view_count']== 0 ].index)
        .reset_index().drop(columns = 'index')
        )
        
    return df_last

def log (df_lastdate):
    df_assign = ( 
        df_lastdate.assign(log_likes=np.log(df_lastdate['likes']))
        .assign(log_views=np.log(df_lastdate['view_count']))
        .assign(log_dislikes=np.log(df_lastdate['dislikes']))
    )
    
    return df_assign
    