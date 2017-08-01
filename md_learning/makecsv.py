import sys
import psycopg2
import numpy as np

def main():
    global cur, conn

    # Connect to DB
    args = sys.argv[1:]
    try:
        conn = psycopg2.connect(host=args[0], database=args[1], user=args[2], password=args[3])
        print('connected')
    except:
        print('Unable to connect to PostgreSQL')
    cur = conn.cursor()

    getquery = """SELECT charges.disposition, cases.court_system, cases.type, cases.filing_date, parties.race, parties.sex, parties.height, parties.weight, parties.state, parties.city, parties.zip, charges.description,
                  FROM cases
                  JOIN parties ON cases.case_id = parties.case_id
                  JOIN charges ON cases.case_id = charges.case_id
                  WHERE NULLIF(cases.disposition, '') IS NOT NULL
        		  AND NULLIF(parties.race, '') IS NOT NULL
        		  AND NULLIF(parties.sex, '') IS NOT NULL
        		  AND NULLIF(parties.zip, '') IS NOT NULL
                  AND LOWER(parties.type) LIKE '%defendant%'"""
    print('query complete')
    dataoutput = "COPY ({0}) TO STDOUT WITH CSV HEADER DELIMITER '|'".format(getquery)
    with open('datafile.csv', 'w') as f:
            cur.copy_expert(dataoutput, f)

    print()


if __name__ == '__main__': main()


'''
JOIN attorneys ON cases.case_id = attorneys.case_id
JOIN events ON cases.case_id = events.case_id
JOIN documents ON cases.case_id = documents.case_id
JOIN judgements ON cases.case_id = judgements.case_id
JOIN complaints ON cases.case_id = complaints.case_id
'''
