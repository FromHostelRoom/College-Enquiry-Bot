from flask import Flask
from backend.db_config import db_config
from flask.json import jsonify
import itertools

def execute_general_query(sql):

	cur = db_config()
	fields = "college_name, affiliation, established, facilities, mhrd, reviews, `type`, city_name, state_name, substream_name,  stream_name, total, duration, course_time, exam_date, exam_name, last_application_date, min_score, seats"
	join = "SELECT %s FROM tbl_college JOIN tbl_city on tbl_college.city_id = tbl_city.city_id JOIN tbl_state on tbl_state.state_id = tbl_city.state_id JOIN tbl_country on tbl_country.country_id = tbl_state.country_id JOIN tbl_fees on tbl_fees.college_id = tbl_college.college_id JOIN tbl_substream on tbl_substream.substream_id = tbl_fees.substream_id JOIN tbl_stream on tbl_substream.stream_id = tbl_stream.stream_id JOIN tbl_eligibility on tbl_eligibility.id = tbl_fees.fees_id " %(fields)

	cur.execute(join+sql) 
	details = []    
	for row in cur.fetchall() :
	    details.append(row)
	
	speak = "Here are the colleges for your query"
	result = [speak,details]
	return jsonify(result)

def execute_specific_query(sql):

	fields = sql[1]
	print("Printing fields to be fetched")
	print(fields)
	cur = db_config()
	#fields = "college_name, affiliation, established, facilities, mhrd, reviews, `type`, city_name, state_name, substream_name,  stream_name, total, duration, course_time, exam_date, exam_name, last_application_date, min_score, seats"
	join = "SELECT %s FROM tbl_college JOIN tbl_city on tbl_college.city_id = tbl_city.city_id JOIN tbl_state on tbl_state.state_id = tbl_city.state_id JOIN tbl_country on tbl_country.country_id = tbl_state.country_id JOIN tbl_fees on tbl_fees.college_id = tbl_college.college_id JOIN tbl_substream on tbl_substream.substream_id = tbl_fees.substream_id JOIN tbl_stream on tbl_substream.stream_id = tbl_stream.stream_id JOIN tbl_eligibility on tbl_eligibility.id = tbl_fees.fees_id " %(fields)

	cur.execute(join+sql[0]) 
	details = []    
	for row in cur.fetchall() :
	    details.append(row)
	
	result = [sql[2],details]
	return jsonify(result)