import pandas as pd


def find(city):
    df = pd.read_csv(
        'D:\Projects\djhack\Therapists\Therapists-{}.csv'.format(city))
    s = df.sample(3, axis=1)
    s = [s.columns.values.tolist()]+s.values.tolist()
    l = []
    for i in range(2):
        d = {'Name': s[0][i],
             'Role': s[3][i],
             'Location': s[4][i],
             'Contact': s[7][i],
             'Email': s[8][i],
             }
        l.append(d)
    return(l)


print(find('mumbai'))
