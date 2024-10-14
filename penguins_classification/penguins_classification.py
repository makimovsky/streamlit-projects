import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

target_mapper = {
    'Adelie': 0,
    'Chinstrap': 1,
    'Gentoo': 2
}


def target_encode(val):
    return target_mapper[val]


df = pd.read_csv('penguins_cleaned.csv')
target = 'species'
encode = ['sex', 'island']

for col in encode:
    dummy = pd.get_dummies(df[col], prefix=col)
    df = pd.concat([df, dummy], axis=1)
    del df[col]

df['species'] = df['species'].apply(target_encode)

X = df.drop('species', axis=1)
Y = df['species']

clf = RandomForestClassifier()
clf.fit(X, Y)

pickle.dump(clf, open('penguins_clf.pkl', 'wb'))
