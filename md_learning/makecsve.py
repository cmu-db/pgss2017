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

    getquery = """SELECT charges.disposition, cases.court_system, cases.type, cases.filing_date, parties.race, parties.sex, parties.height, parties.weight, parties.state, parties.city, SUBSTR(parties.zip, 1, 5) AS zip, charges.description, charges.fine_amt
                  FROM cases
                  JOIN parties ON cases.case_id = parties.case_id
                  JOIN charges ON cases.case_id = charges.case_id
                  WHERE NULLIF(charges.disposition, '') IS NOT NULL
                  AND NULLIF(cases.court_system, '') IS NOT NULL
                  AND NULLIF(cases.type, '') IS NOT NULL
                  AND cases.filing_date IS NOT NULL
                  AND NULLIF(parties.race, '') IS NOT NULL
                  AND NULLIF(parties.sex, '') IS NOT NULL
                  AND charges.fine_amt IS NOT NULL
                  AND parties.height IS NOT NULL
                  AND parties.weight IS NOT NULL
                  AND NULLIF(parties.state, '') IS NOT NULL
                  AND NULLIF(parties.city, '') IS NOT NULL
                  AND NULLIF(parties.zip, '') IS NOT NULL
                  AND NULLIF(charges.description, '') IS NOT NULL
                  AND LOWER(parties.type) LIKE '%defendant%'
                  AND LENGTH(parties.zip) = 5
                """
    dataoutput = "COPY ({0}) TO STDOUT WITH CSV HEADER DELIMITER '|'".format(getquery)
    with open('datafile.csv', 'w') as f:
            cur.copy_expert(dataoutput, f)
            print('query complete')



if __name__ == '__main__': main()


'''
#CODE TO ADD OTHER TABLES
JOIN attorneys ON cases.case_id = attorneys.case_id
JOIN events ON cases.case_id = events.case_id
JOIN documents ON cases.case_id = documents.case_id
JOIN judgements ON cases.case_id = judgements.case_id
JOIN complaints ON cases.case_id = complaints.case_id
'''
