import sys
import psycopg2
import numpy as np


global cur, conn

# Connect to DB
args = sys.argv[1:]
try:
    conn = psycopg2.connect(host=args[0], database=args[1], user=args[2], password=args[3])
    print('connected')
except:
    print('Unable to connect to PostgreSQL')
cur = conn.cursor()


def civiltype():
    getquery = """SELECT type
                  FROM cases
                  WHERE LOWER(court_system) LIKE '%civil%'
                  AND LOWER(court_system) NOT LIKE '%civil citation%'
                  GROUP BY type
                """


    cur.execute(getquery)
    civil_case_type = cur.fetchall()
    masterString = "CIVIL"

    for element in civil_case_type:
        x = ("'%s'," % element[0])
        masterString = masterString + x + " "

    print("civil types are: " + masterString)
    with open('types.csv', 'w') as f:
            f.write(masterString + '\n')
            print('query complete')


def criminaltype():
    getquery = """SELECT type
                  FROM cases
                  WHERE LOWER(court_system) LIKE '%criminal%'
                  GROUP BY type
               """

    cur.execute(getquery)
    civil_case_type = list(cur.fetchall())
    masterString = "CRIMINAL"

    for element in civil_case_type:
        x = ("'%s'," % element[0])
        masterString = str(masterString + x + " ")

    print("criminal types is: " + masterString)
    with open('types.csv', 'a') as f:
            f.write(masterString + '\n')
            print('query complete')

def citationtype():
    getquery = """SELECT type
                  FROM cases
                  WHERE LOWER(court_system) LIKE '%civil citation%'
                  GROUP BY type
               """

    cur.execute(getquery)
    civil_case_type = list(cur.fetchall())
    masterString = "CIVILCITATION"

    for element in civil_case_type:
        x = ("'%s'," % element[0])
        masterString = str(masterString + x + " ")

    print("citation types are: " + masterString)
    with open('types.csv', 'a') as f:
            f.write(masterString + '\n')
            print('query complete')

def traffictype():
    getquery = """SELECT type
                  FROM cases
                  WHERE LOWER(court_system) LIKE '%traffic%'
                  GROUP BY type
               """

    cur.execute(getquery)
    civil_case_type = list(cur.fetchall())
    masterString = "TRAFFIC"

    for element in civil_case_type:
        x = ("'%s'," % element[0])
        masterString = str(masterString + x + " ")

    print("traffic types are: " + masterString)
    with open('types.csv', 'a') as f:
            f.write(masterString + '\n')
            print('query complete')


def main():
    civiltype()
    criminaltype()
    traffictype()
    citationtype()








if __name__ == '__main__': main()
