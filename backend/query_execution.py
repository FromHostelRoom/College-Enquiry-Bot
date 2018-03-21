from flask import Flask
from backend.db_config import db_config


def execute_query(sql):

	cur = db_config()
	fields = "college_name, affiliation, established, facilities, rank, reviews, `type`, city_name, state_name, substream_name,  stream_name, total, duration, course_time, exam_date, exam_name, last_application_date, min_score, seats"
	join = "SELECT %s FROM credenc_college JOIN credenc_city on credenc_college.city_id = credenc_city.city_id JOIN credenc_state on credenc_state.state_id = credenc_city.state_id JOIN credenc_fees on credenc_fees.college_id = credenc_college.college_id JOIN credenc_substream on credenc_substream.substream_id = credenc_fees.substream_id JOIN credenc_stream on credenc_substream.stream_id = credenc_stream.stream_id JOIN credenc_eligibility on credenc_eligibility.id = credenc_fees.fees_id" %(fields)

	cur.execute(join+sql) 
	details = []    
	for row in cur.fetchall() :
	    details += row
	    print (row)
	return details