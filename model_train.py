import pandas as pd
from numpy.random import RandomState
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle

filename = 'finalized_model.pkl'

df3 = pd.read_csv('df3.csv', converters={'emotions': eval})

rng = RandomState()

train = df3.sample(frac=0.7, random_state=rng)
test = df3.loc[~df3.index.isin(train.index)]

X_train, X_test, y_train, y_test = train_test_split(df3['text'].values.astype('U'), df3['final_cat'].values.astype('U'), random_state=1)

cv = CountVectorizer(strip_accents='ascii', lowercase=True, stop_words='english')
X_train_cv = cv.fit_transform(X_train)
X_test_cv = cv.transform(X_test)

naive_bayes = MultinomialNB()
naive_bayes.fit(X_train_cv, y_train)
predictions = naive_bayes.predict(X_test_cv)

print("Accuracy score: ", accuracy_score(y_test, predictions))

pickle.dump(naive_bayes, open(filename, 'wb'))