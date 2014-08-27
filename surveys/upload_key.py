import os
import psycopg2 as pg
from models import Base


PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(PROJECT_DIR, 'raw')

conn = pg.connect(database="aa_surveys", user="postgres", password="joseph", host='127.0.0.1')
cur = conn.cursor()

def main():
	print "Enter the filename for the survey key"
	filename = raw_input()
	if ".csv" not in filename: filename = filename + ".csv"
	print "Enter the sql table name the survey key should be copied to"
	tableList = []
	for t in Base.metadata.sorted_tables:
		tableList.append(t.name)
		print t.name
	tablename = raw_input()
	while tablename not in tableList:
		print "Invalid choice"
		tablename = raw_input()

	statement = "COPY {} from '{}' DELIMITER ',' CSV HEADER;".format(tablename, os.path.join(PROJECT_DIR, filename))
	cur.execute(statement)
	conn.commit()

if __name__ == "__main__":
	main()

