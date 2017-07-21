import psycopg2
from parser import parseCase

# EXAMPLE: python3 main.py localhost test user password

# Connect to DB
args = sys.argv[1:]
try:
    conn = psycopg2.connect(host=args[0], database=args[1], user=args[2], password=args[3])
except:
    print('Unable to connect to PostgreSQL')
cur = conn.cursor()

# Get raw case HTML
cur.execute('SELECT html FROM rawcases')
for case in cur:
    data = parseCase(case.html)
    # TODO: Insert into DB
