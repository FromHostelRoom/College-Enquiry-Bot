from flask import Flask
import MySQLdb

def db_config():

	db = MySQLdb.connect(host='localhost',
	                     user='root',
	                     passwd='',
	                     db='',
	                     charset='utf8',
	                     use_unicode=True)
	cur = db.cursor()
	return cur