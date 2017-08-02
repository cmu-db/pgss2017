from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np
import graphviz
from sklearn.tree import export_graphviz
import sys
import pandas as pd

le= LabelEncoder()

count = 0
guilty = ['Guilty',  'Guilty - Prepaid',  'Nolo Contendere',  'Probation Before Judgment',  'Probation Before Judgment - 292',  'Probation Before Judgment - 641',  'Probation Before Judgment - Supervised',  'Probation Before Judgment - Unsupervised']
notguilty = ['Abated by Death',  'Compromise',  'Court Dismissed Case',  'Dismissed',  'Judgment of Acquittal',  'Nolle Prosequi',  'Not Guilty']
inprocess = ['Forwarded - Circuit Court',  'Jury Trial Prayed',  'Merged',  'Merged with a Related Citation',  'Stet']
def main():
    #reads original datafile from csv
    courtdata = open('datafile.csv',  'r')
    #creates new outputfile for grouped data
    outputfile = open('outputfile.csv',  'w')


    for row in courtdata:
        row = row.replace(',', ' ')
        data = row.split('|')
        disptemp = data[0]
        restdata = data[1:11]
        if ':'  in disptemp:
            disp = disptemp.split(':')
            if disp[1] in guilty:
                fieldval='guilty'
            elif disp[1] in notguilty:
                fieldval='not-guilty'
            else:
                fieldval='in-process'
            #restdata.insert(0,  disp[1])
            restdata.insert(0, fieldval)
        else:
            if disptemp in guilty:
                fieldval='guilty'
            elif disptemp in notguilty:
                fieldval='not-guilty'
            else:
                fieldval='in-process'
            restdata.insert(0, fieldval)

        outdata = ','.join([str(item) for item in restdata])
        outputfile.write(outdata+'\n')
    outputfile.close()


    csv = pd.read_csv('outputfile.csv',  delimiter= ',')
    for col in csv.columns.values:
        if csv[col].dtype == 'object':
            output = csv[col]
            le.fit(output.values)
            csv[col]= le.transform(csv[col])
    data = csv.iloc[1: , 1:]
    target = csv.iloc[1:,  0]
    feature_names = csv.iloc[0,  1:]
    print ('class names are: ',  target.values)

    #Code to create decision tree
    X_train,  X_test,  y_train,  y_test = train_test_split(data,  target,  test_size = .33)
    tree = DecisionTreeClassifier(max_depth=4,  random_state=0) # pre pruned tree limiting depth
    tree.fit(X_train,  y_train)
    print('Accuracy on the training subset: {:.3f}'.format(tree.score(X_train,  y_train)))
    print('Accuracy on the test subset: {:.3f}'.format(tree.score(X_test,  y_test)))
        #fix line (csv flie?)
    export_graphviz(tree,  out_file='dispositiontree.dot',   feature_names=feature_names.index,   impurity=False,  filled=True)

if __name__ == '__main__': main()
