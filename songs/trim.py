import pandas as pd
df = pd.read_csv('songdata.csv')
check = df['mood'] == 0
df_0 = df[check]
df_0.to_csv('happysongs.csv')
check2 = df['mood'] == 1
df_1 = df[check2]
df_1.to_csv('sadsongs.csv')


def song():
    k = df_0.sample(1)[['artist', 'song', 'link']]
    s = k.to_dict('list')
    return s


def sadsong():
    l = df_1.sample(1)[['artist', 'song', 'link']]
    m = l.to_dict('list')
    return m


print(song())
print(sadsong())
