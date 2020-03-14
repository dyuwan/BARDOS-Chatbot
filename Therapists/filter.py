import pandas as pd
def filtering(city):
    df = pd.read_csv('/Users/dyuwan/Downloads/Therapists-{}.csv'.format(city))
    df=df.head(8)
    for k in df.head(1):
        if "Unnamed" in k:
            df.drop(k, axis = 1, inplace = True)
    df.to_csv('/Users/dyuwan/Downloads/Therapists-{}.csv'.format(city))
            
filtering("Hyderabad")