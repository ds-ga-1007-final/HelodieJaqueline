import pandas as pd


def clean_nan(data):
    #data=data[['DATE','TIME','BOROUGH','NUMBER OF PERSONS INJURED','NUMBER OF PERSONS KILLED','NUMBER OF PEDESTRIANS INJURED','NUMBER OF PEDESTRIANS KILLED','NUMBER OF CYCLIST INJURED','NUMBER OF CYCLIST KILLED','NUMBER OF MOTORIST KILLED','NUMBER OF MOTORIST INJURED','UNIQUE KEY' ,'Date','time']]
    data=data.dropna(subset=['BOROUGH'])
    return data
def add_time(data):
    
    return data


def hasInjuredORkilled(data):
    list_t=data['TIME']
    time=pd.to_datetime(list_t, format='%H:%M')
    
    data_inj=data[['NUMBER OF PERSONS INJURED','NUMBER OF PEDESTRIANS INJURED','NUMBER OF CYCLIST INJURED','NUMBER OF MOTORIST KILLED','NUMBER OF MOTORIST INJURED']]
    inj=data_inj.sum(axis=1)
    data_ki=data[['NUMBER OF PERSONS KILLED','NUMBER OF PEDESTRIANS KILLED','NUMBER OF CYCLIST KILLED','NUMBER OF MOTORIST KILLED']]
    killed=data_ki.sum(axis=1)
    df=data[['NUMBER OF PERSONS INJURED','NUMBER OF PERSONS KILLED','NUMBER OF PEDESTRIANS INJURED','NUMBER OF PEDESTRIANS KILLED','NUMBER OF CYCLIST INJURED','NUMBER OF CYCLIST KILLED','NUMBER OF MOTORIST KILLED','NUMBER OF MOTORIST INJURED']]
    df_sum=df.sum(axis=1)
    data['time']=time
    data['HAS INJURED']=inj
    data['HAS KILLED']=killed
    data['HAS INJURED OR KILLED']=df_sum
    return data

