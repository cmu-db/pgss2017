import sys
import psycopg2
import numpy as np

def main():
    global cur, conn

    # Connect to DB
    args = sys.argv[1:]
    try:
        conn = psycopg2.connect(host=args[0], database=args[1], user=args[2], password=args[3])
    except:
        print('Unable to connect to PostgreSQL')
    cur = conn.cursor()

    getquery = '''SELECT cases.disposition, parties.race, parties.sex, parties.zip, charges.injuries, charges.property_damage
                  FROM cases
                  JOIN parties ON cases.case_id = parties.case_id
                  JOIN charges ON cases.case_id = charges.case_id
                  WHERE NULLIF(cases.disposition, '') IS NOT NULL'''

    dataoutput = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(getquery)

    with open('datafile.csv', 'w') as f:
            cur.copy_expert(dataoutput, f)
