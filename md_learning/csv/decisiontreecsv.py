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

#### simplyfy case types to guilty, not guilty and inprocess ####
guilty = ['Guilty',  'Guilty - Prepaid',  'Nolo Contendere']
notguilty = ['Abated by Death',  'Compromise',  'Court Dismissed Case',  'Dismissed',  'Judgment of Acquittal',  'Nolle Prosequi',  'Not Guilty']
inprocess = ['Probation Before Judgment',  'Probation Before Judgment - 292',  'Probation Before Judgment - 641',  'Probation Before Judgment - Supervised',  'Probation Before Judgment - Unsupervised', 'Forwarded - Circuit Court',  'Jury Trial Prayed',  'Merged',  'Merged with a Related Citation',  'Stet']

#### simplyfy race to white, black, asian and others ####
black = ['BLACK, AFRICAN AMERICAN', 'BLACK,AFRICAN AMERICAN', 'Black', 'BLACK', 'African American', 'Black', 'African American', 'African American/Black', ]
white = ['White', 'Caucasian', 'WHITE', 'Caucasion']
asian = ['Asian', 'Other Asian', 'ASIAN, NATIVE HAWAIIAN,OTHER PACIFIC ISLANDER', 'ASIAN, NATIVE HAWAIIAN, OTHER PACIFIC ISLANDER', 'Native Hawaiian or Other Pacific Islander', 'INDIAN']
hispanic = ['Hispanic']
other = ['WHITE, CAUCASIAN, ASIATIC INDIAN, ARAB', 'WHITE,CAUCASIAN,ASIATIC INDIAN,ARAB', 'UNKNOWN,OTHER', 'Other', 'UNKNOWN, OTHER',  'Unavailable', 'AMERICAN INDIAN, ALASKA NATIVE', 'Indian', 'UNKNOWN',  'AMERICAN INDIAN,ALASKA NATIVE', 'Unknown', 'OTHER']

### simplyfy court type to civil criminal traffic ###
criminalcourt = [' Criminal System', ' Criminal']
trafficcourt = [' Traffic System']
civilcourt = [' ']

### initialize the list for case types. Data will come from list created from DB ###
crimcase=[]
civilcase=[]
trafficcase=[]
citationcase=[]
def main():
    typedata = open('types.csv',  'r')
    for row in typedata:
        temp = row.split(',')
        head=temp[0]
        data=temp[1:]
        if  head == "CRIMINAL'None'":
            for item in data:
                if item.strip() not in ['\n',  '']:
                    crimcase.insert(0, item.replace("'", '').strip())
        if  head == "CIVIL'None'":
            for item in data:
                if item.strip() not in ['\n',  '']:
                    civilcase.insert(0, item.replace("'", '').strip())
        if  head == "TRAFFIC'None'":
            for item in data:
                if item.strip() not in ['\n',  '']:
                    trafficcase.insert(0, item.replace("'", '').strip())
        if  head == "CIVIL CITATIONS'None'":
            for item in data:
                if item.strip() not in ['\n',  '']:
                    citationcase.insert(0, item.replace("'", '').strip())

    #### open files  for processing ####
    courtdata = open('datafile.csv',  'r')
    outputfile = open('outputfile.csv',  'w')
    #inprocessfile = open('inprocess.csv',  'w')

    courttype = 'courttype'

    #### cleanup and simplify file from DB ####
    for row in courtdata:
        restdata=[]
        row = row.replace(',', ' ')
        data = row.split('|')

        disptemp = data[0]

        tempcourt = data[1]
        court=tempcourt.split('-')
        courtnametemp = court[0]

        if len(court) > 1:
            courttypetemp = court[1]
            if courttypetemp in criminalcourt:
                courttypetemp = 'criminal'
            elif courttypetemp in trafficcourt:
                courttypetemp = 'traffic'

        type = data[2]
        race = data[4]
        sex = data[5]
        #restdata = data[5:9]
        state=data[8]
        ziptemp = data[10]
        newzip = ziptemp[:3]

        if type in crimcase:
            type = 'criminal'
        elif type in civilcase:
            type = 'civil'
        elif type in trafficcase:
            type = 'traffic'
        elif type in citationcase:
            type = 'citation'

        if race in black:
            race = 'black'
        elif race in white:
            race = 'white'
        elif race in asian:
            race = 'asian'
        elif race in hispanic:
            race = 'hispanic'
        elif race in other:
            race = 'other'

        if courtnametemp == 'court_system':
            courtname = 'courtname'
        else:
            courtname = courtnametemp

        if len(court) > 1:
            courttype = courttypetemp

        restdata.insert(0,  state)
        restdata.insert(0,  sex)
        restdata.insert(0,  race)
        restdata.insert(0,  type)
        restdata.insert(0, courtname)
        restdata.insert(0, courttype)

        if ':'  in disptemp:
            disp = disptemp.split(':')
            if disp[1] in guilty:
                fieldval='guilty'
            elif disp[1] in notguilty:
                fieldval='not-guilty'
            else:
                fieldval='in-process'
            restdata.insert(0, fieldval)
            restdata.insert(7,  newzip)
        else:
            if disptemp in guilty:
                fieldval='guilty'
            elif disptemp in notguilty:
                fieldval='not-guilty'
            elif disptemp in inprocess:
                fieldval='in-process'
            else:
                fieldval=disptemp
            restdata.insert(0, fieldval)
            restdata.insert(7,  newzip)

    #### seperate out cases that are already decided ####
        if  (restdata[0] in ['guilty',  'not-guilty',  'disposition']):
            if restdata[7].isdigit() is True or restdata[7] in ['zip']:
                outdata = ','.join([str(item) for item in restdata])
                outputfile.write(outdata+'\n')

    #### seperate out cases that are still in process for possible prediction later ####
#    if (restdata[0] in ['in-process',  'disposition']):
#        inprocessdata = ','.join([str(item) for item in restdata])
#        inprocessfile.write(inprocessdata+'\n')

    outputfile.close()
    #inprocessfile.close()

    #### pre process simplified file to convert to a format friendly to decision tree classifier ####
    csv = pd.read_csv('outputfile.csv',  delimiter= ',')
    for col in csv.columns.values:
        if csv[col].dtype == 'object':
            output = csv[col]
            le.fit(output.values)
            csv[col]= le.transform(csv[col])
    #print (type(output))
    #print (csv.head())
    data = csv.iloc[1: , 1:]
    target = csv.iloc[1:,  0]
    feature_names = csv.iloc[0,  1:]
    #print ('class names are: ',  feature_names.index)

    #### Code to create decision tree####
    X_train,  X_test,  y_train,  y_test = train_test_split(data,  target,  test_size = .33)
    tree = DecisionTreeClassifier(max_depth=5,  random_state=0) # pre pruned tree limiting depth
    tree.fit(X_train,  y_train)
    print('Accuracy on the training subset: {:.3f}'.format(tree.score(X_train,  y_train)))
    print('Accuracy on the test subset: {:.3f}'.format(tree.score(X_test,  y_test)))

    ####  Create Decision Tree Graph using graphviz ####
    export_graphviz(tree,  out_file='dispositiontreecsv.dot', class_names=['guilty',  'not guilty'],  feature_names=feature_names.index,   impurity=False,  filled=True)
    n_features = data.shape[1]
    plt.barh(range(n_features),  tree.feature_importances_,  align='center')
    plt.yticks(np.arange(n_features),  feature_names.index)
    plt.xlabel('Feature Importances')
    plt.ylabel('Feature')
    plt.show()

if __name__ == '__main__': main()
