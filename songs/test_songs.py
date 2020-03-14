import pickle
import pandas as pd
loaded_model = pickle.load(open('./lyrics_clf_1000_py.pkl', 'rb'))
df = pd.read_csv('/Users/dyuwan/Downloads/songdata.csv')
z = df['text'].values
result = loaded_model.predict(z)
df['mood']=result
print(result)
df.to_csv('/Users/dyuwan/Downloads/songdata.csv')