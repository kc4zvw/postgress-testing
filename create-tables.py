#!/usr/local/bin/python
#
# $Id:$

import psycopg2
from configparser import ConfigParser
 
def config(filename='database2.ini', section='postgresql'):
	# create a parser
	parser = ConfigParser()
	# read config file
	parser.read(filename)

	# get section, default to postgresql
	db = {}
	if parser.has_section(section):
		params = parser.items(section)
		for param in params:
			db[param[0]] = param[1]
			#print("%s = %s" % (param[0], param[1]))
	else:
		raise Exception('Section {0} not found in the {1} file'.format(section, filename))

	return db

def create_tables():
	""" create tables in the PostgreSQL database """
	commands = (
		"""
		CREATE TABLE IF NOT EXISTS vendors (
			vendor_id SERIAL PRIMARY KEY,
			vendor_name VARCHAR(255) NOT NULL
		)
		""",
		""" CREATE TABLE IF NOT EXISTS parts (
				part_id SERIAL PRIMARY KEY,
				part_name VARCHAR(255) NOT NULL
				)
		""",
		"""
		CREATE TABLE IF NOT EXISTS part_drawings (
				part_id INTEGER PRIMARY KEY,
				file_extension VARCHAR(5) NOT NULL,
				drawing_data BYTEA NOT NULL,
				FOREIGN KEY (part_id)
				REFERENCES parts (part_id)
				ON UPDATE CASCADE ON DELETE CASCADE
		)
		""",
		"""
		CREATE TABLE IF NOT EXISTS vendor_parts (
				vendor_id INTEGER NOT NULL,
				part_id INTEGER NOT NULL,
				PRIMARY KEY (vendor_id , part_id),
				FOREIGN KEY (vendor_id)
					REFERENCES vendors (vendor_id)
					ON UPDATE CASCADE ON DELETE CASCADE,
				FOREIGN KEY (part_id)
					REFERENCES parts (part_id)
					ON UPDATE CASCADE ON DELETE CASCADE
		)
		""")
	conn = None
	try:
		# read the connection parameters
		params = config()
		# connect to the PostgreSQL server
		conn = psycopg2.connect(**params)

		cur = conn.cursor()
		# create table one by one
		for command in commands:
			cur.execute(command)
		# close communication with the PostgreSQL database server
		cur.close()
		# commit the changes
		conn.commit()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()
			print('Finished.')
 
if __name__ == '__main__':
	create_tables()

# End of script
