import sys
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
    results = np.array(cur.fetchall())

    courtcsv = np.genfromtxt('courtdatafile.csv', delimiter =',', converters={1:myconv})



    #getquery = '''SELECT *
    #              FROM cases, parties, attorneys, events, charges, documents, judgements, complaints
    #              WHERE case.id = case_id
    #              GROUP BY case_id''')

    #dataoutput = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(getquery)
    #with open('datafile.csv', 'w') as f:
    #        cur.copy_expert(dataoutput, f)
