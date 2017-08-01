import psycopg2
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np
import graphviz
from sklearn.tree import export_graphviz
import sys

def myconv(x):
    if x.decode("utf-8") == "guilty":
        a = 1
        return float(a)
    else:
        a = 0
        return float(a)

def main():
    csv = np.genfromtxt('datafile.csv', dtype='float', skip_header = 1, delimiter ='|', converters={0:myconv})
    ar = np.array(csv, dtype='f')
    with open('datafile2.csv', 'w') as f:
            f.write(str(ar))

    data = ar[:, 1:]
    target = ar[0:, 1]

    #Code to create decision tree
    X_train,  X_test,  y_train,  y_test = train_test_split(data,  target,  test_size = .33)
    tree = DecisionTreeClassifier(max_depth=4,  random_state=0) # pre pruned tree limiting depth
    tree.fit(X_train,  y_train)
    print('Accuracy on the training subset: {:.3f}'.format(tree.score(X_train,  y_train)))
    print('Accuracy on the test subset: {:.3f}'.format(tree.score(X_test,  y_test)))
    #fix line (csv flie?)
    export_graphviz(tree,  out_file='dispositiontree.dot',  class_names=['Guilty',  'Not Guilty'],  feature_names=csv.feature_names,  impurity=False,  filled=True)


if __name__ == '__main__': main()
