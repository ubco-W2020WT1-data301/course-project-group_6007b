import pandas as pd
import numpy as np
import datetime
import pandas_profiling
import seaborn as sns
import matplotlib.pylab as plt
import glob

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
            .replace({"categoryId":category_replace})
            .drop(df[df['categoryId']=='NaN'].index).sort_values('trending_date')
            .reset_index().drop(columns = ['index'])
    )
        
    df_last = (
        pd.DataFrame(data=df_clean)
        .drop_duplicates(['video_id'], keep='last').reset_index().drop(columns = 'index')
        )
        
    return df_last