import psycopg2
import courtdatafile.csv
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np
import graphviz
from sklearn.tree import export_graphvizimport sys

def myconv(x):
    if x.decode("utf-8") == "guilty":
        a = 1
        return float(a)
    else:
        a = 0
        return float(a)

def main():
    global cur, conn

    # Connect to DB
    args = sys.argv[1:]
    try:
        conn = psycopg2.connect(host=args[0], database=args[1], user=args[2], password=args[3])
    except:
        print('Unable to connect to PostgreSQL')
    cur = conn.cursor()

    #select data from DB
    with cur:
        cur.execute('''SELECT cases.disposition, parties.race, parties.sex, parties.zip, charges.injuries, charges.property_damage
                 FROM cases
                 JOIN parties ON cases.case_id = parties.case_id
                 JOIN charges ON cases.case_id = charges.case_id
                 WHERE NULLIF(cases.disposition, '') IS NOT NULL''')
        results = np.array(cur.fetchall())
        print(results)
        data = results[:, 1:]
        target = myconv(results[1, :])

    #Code to create decision tree
    X_train,  X_test,  y_train,  y_test = train_test_split(data,  target,  test_size = .33)
    tree = DecisionTreeClassifier(max_depth=4,  random_state=0) # pre pruned tree limiting depth
    tree.fit(X_train,  y_train)
    print('Accuracy on the training subset: {:.3f}'.format(tree.score(X_train,  y_train)))
    print('Accuracy on the test subset: {:.3f}'.format(tree.score(X_test,  y_test)))
    #fix line (csv flie?)
    export_graphviz(tree,  out_file='dispositiontree.dot',  class_names=['Guilty',  'Not Guilty'],  feature_names=cancer.feature_names,  impurity=False,  filled=True)


if __name__ == '__main__': main()
