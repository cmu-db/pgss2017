import sys
import psycopg2
from parser import parseCase

# EXAMPLE: python3 main.py localhost test user password

# Field tuples for each table
TABLE_COLS = {
    'cases': ('case_id', 'title', 'court_system', 'type', 'filing_date', 'status', 'disposition', 'disposition_date', 'violation_county', 'violation_date'),
    'parties': ('case_id', 'name', 'type', 'bus_org_name', 'agency_name', 'race', 'sex', 'height', 'weight', 'dob', 'address', 'city', 'state', 'zip'),
    'attorneys': ('case_id', 'name', 'type', 'appearance_date', 'removal_date', 'practice_name', 'address', 'city', 'state', 'zip'),
    'events': ('case_id', 'type', 'date', 'time', 'result', 'result_date'),
    'charges': ('case_id', 'statute_code', 'description', 'offense_date_from', 'offense_date_to', 'class', 'amended_date', 'cjis_code', 'probable_cause', 'victim_age', 'speed_limit', 'recorded_speed', 'location_stopped', 'accident_contribution', 'injuries', 'property_damage', 'seatbelts_used', 'mandatory_court_appearance', 'vehicle_tag', 'state', 'plea', 'plea_date', 'disposition', 'disposition_date', 'jail_extreme_punishment', 'jail_term', 'jail_suspended_term', 'jail_unsuspended_term', 'probation_term', 'probation_supervised_term', 'probation_unsupervised_term', 'fine_amt', 'fine_suspended_amt', 'fine_restitution_amt', 'fine_due', 'fine_first_pmt_due', 'cws_hours', 'cws_deadline', 'cws_location', 'cws_date'),
    'documents': ('case_id', 'name', 'filing_date'),
    'judgements': ('case_id', 'against', 'in_favor_of', 'type', 'date', 'interest', 'amt'),
    'complaints': ('case_id', 'type', 'against', 'status', 'status_date', 'filing_date', 'amt')
}

def main():
    global cur, conn

    # Connect to DB
    args = sys.argv[1:]
    try:
        conn = psycopg2.connect(host=args[0], database=args[1], user=args[2], password=args[3])
    except:
        print('Unable to connect to PostgreSQL')
    cur = conn.cursor()

    # This is only for testing
    if len(args) > 4 and args[4] == 'test':
        insertCase(open('test.html', 'r').read())
    else:
        # Get raw case HTML where we haven't already parsed it
        cur.execute('SELECT * FROM rawcases WHERE case_id NOT IN (SELECT case_id FROM cases) ORDER BY case_id')

        # Apply case limit
        if len(args) > 4 and args[4].isdigit():
            limit = int(args[4])
        else:
            limit = None

        # Iterate thru cases
        i = 0
        for case in cur:
            insertCase(case[1])
            i += 1
            if limit and i >= limit:
                break

# Insert all the data for a case
def insertCase(html):
    # Parse HTML
    data = parseCase(html)
    # Store case ID
    case_id = data['cases'][0]['case_id']
    # Insert data for each section/table
    for section in data:
        for entry in data[section]:
            insertData(case_id, entry, section)

# Insert a row into a table
def insertData(case_id, data, table):
    # Get the value for a field
    def getFieldValue(field):
        if field == 'case_id':
            return case_id
        else:
            return data.get(field) or None

    # Make sure data for this table exists
    if data:
        # Build tuple of col values
        dataFields = TABLE_COLS[table]
        dataTuple = tuple(getFieldValue(field) for field in dataFields)

        # Execute insertion
        cur.execute('INSERT INTO ' + table + ' ' + str(dataFields).replace('\'', '') + ' VALUES (' + '%s, ' * (len(dataFields) - 1) + '%s)', dataTuple)
        print('Saved %s row for %s' % (table, case_id))

    # Commit changes to DB
    conn.commit()

if __name__ == '__main__': main()
