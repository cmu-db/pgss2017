import psycopg2
import numpy as np


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
    with cur :
        sql = '''SELECT cases.disposition, parties.race, parties.sex, parties.zip, charges.injuries, charges.property_damage FROM cases JOIN parties JOIN charges
                 WHERE cases.dispostion IN {}
                 ORDER BY cases.disposition'''.format(tuple(cases.dispostion))
        cursor.execute(sql)
        all = np.array(cursor.fetchall())
        print(all)
        arr = dict()
        for i, cases.disposition in enumerate(cases.disposition):
            arr[cases.disposition] = data[i]
        return arr
        print(arr)

        data = arr[:, 1:]
        target = myconv(arr[1, :])
        
    #Code to create decision tree
    X_train,  X_test,  y_train,  y_test = train_test_split(data,  target,  test_size = .33)
    tree = DecisionTreeClassifier(max_depth=4,  random_state=0) # pre pruned tree limiting depth
    tree.fit(X_train,  y_train)
    print('Accuracy on the training subset: {:.3f}'.format(tree.score(X_train,  y_train)))
    print('Accuracy on the test subset: {:.3f}'.format(tree.score(X_test,  y_test)))
#
