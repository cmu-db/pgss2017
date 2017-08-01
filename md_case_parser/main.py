import sys
import psycopg2
from parser import parseCase

# EXAMPLE: python3 main.py localhost test user password 10

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
        print('Connected to PostgreSQL', end='')
    except:
        print('Unable to connect to PostgreSQL')
    cur = conn.cursor()

    # This is only for testing
    if len(args) > 4 and args[4] == 'test':
        insertCase(open('test.html', 'r').read())
    else:
        # Apply query args
        limit = int(args[4])
        if len(args) > 5 and args[5].isdigit():
            offset = int(args[5])
        else:
            offset = None

        # Get raw case HTML where we haven't already parsed it
        cur.execute('SELECT rawcases.case_id, html FROM rawcases LEFT OUTER JOIN cases ON rawcases.case_id = cases.case_id WHERE cases.case_id IS NULL ORDER BY rawcases.case_id LIMIT %s OFFSET %s', (limit, offset))

        # Iterate thru cases
        results = cur.fetchall()
        for i in range(len(results)):
            print('\n[%s remaining]' % (len(results) - i), end=' ')
            insertCase(*results[i])

    print('\n[Done]')

# Insert all the data for a case
def insertCase(raw_case_id, html):
    print('%s...' % raw_case_id)
    # Parse HTML
    data = parseCase(html)
    # Store case ID
    try:
        case_id = data['cases'][0]['case_id']
    except KeyError:
        # Delete the case if it's nonsense
        cur.execute('DELETE FROM rawcases WHERE case_id = %s', (raw_case_id, ))
        print('\nDeleted: nonsense')
        conn.commit()
        return
    # Insert data for each section/table
    for section in data:
        for entry in data[section]:
            result = insertData(raw_case_id, case_id, entry, section)
            if not result: return

# Insert a row into a table
def insertData(raw_case_id, case_id, data, table):
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
        try:
            cur.execute('INSERT INTO ' + table + ' ' + str(dataFields).replace('\'', '') + ' VALUES (' + '%s, ' * (len(dataFields) - 1) + '%s)', dataTuple)
            print(table, end=' ')
        except Exception as error:
            conn.rollback()
            print('\nError inserting %s row' % table, case_id)
            cur.execute('DELETE FROM rawcases WHERE case_id = %s', (raw_case_id,))
            print('\nDeleted: duplicate')
            conn.commit()
            return False

    # Commit changes to DB
    conn.commit()
    return True

if __name__ == '__main__': main()
