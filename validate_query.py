from logic import return_label

def query_validation(message):
	array = ['colleges', 'college', 'university', 'universities', 'campus', 'campuses', 'schools', 'school', 'IIT', 'IIM', 'IIIT', 'NIT']
	
	for i in array:
		if i in message:
			flag = 1
			break
		else:
			flag = 0

	if flag == 1:
		label = return_label(message)
		return label
	else:
		return "Sorry, no data available."
	