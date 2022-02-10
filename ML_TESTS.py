from sklearn import tree
from sklearn import metrics
from sklearn.model_selection import cross_validate
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold

import pandas as pd

data_train = pd.read_csv('train_iris_1.csv')
data_test = pd.read_csv('test_iris_1.csv')
data_all = pd.read_csv('all_two_iris_1.csv')
clf = tree.DecisionTreeClassifier()


X_train = data_train[['sepal.length', 'sepal.width', 'petal.length', 'petal.width']]
y_train = data_train['class']

X_test = data_test[['sepal.length', 'sepal.width', 'petal.length', 'petal.width']]
y_test = data_test['class']

X = data_all[['sepal.length', 'sepal.width', 'petal.length', 'petal.width']]
y = data_all['class']

#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)
clf = clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
print("Accuracy:", metrics.accuracy_score(y_test, y_pred))

"""
cv = cross_validate(clf, X, y, cv=10)
print(cv['test_score'])
print(cv['test_score'].mean())
"""
