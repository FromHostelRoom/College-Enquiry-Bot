from flask import Flask
from collections import Counter
from nltk.tokenize import word_tokenize
from backend.db_config import db_config


def get_college_name(col_name):
	
	cur = db_config()
	res = []
	try:
		tokens = word_tokenize(col_name)
		for i in tokens:
			cur.execute("SELECT `college_name` FROM credenc_college where college_name like '%%%s%%' order by `rank`" % (i))
			l = cur.fetchall()
			res += list(l)

		common = Counter(res)

		college_name = common.most_common(1)[0][0]
		#import pdb;pdb.set_trace()
		return college_name
	except:
		return "Sorry! no colleges available"
	#import pdb;pdb.set_trace()