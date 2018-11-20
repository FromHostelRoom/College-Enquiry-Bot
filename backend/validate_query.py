from backend.classify_query import return_label
from backend.ner import get_sql


def query_validation(msg):
	
	message = (msg.replace(".","")).lower()
	label = return_label(message)
	print(label)
	
	if(label == "general"):
		ner_dataset = "backend/training_data/general/ner_general_query_dataset.txt"
		model_file = "backend/trained_data/general/general_tflearn_logs"
		model_save = "backend/trained_data/general/general_model.tflearn"
		dump = "backend/trained_data/general/general_trained_data"
		sql_dataset = "backend/training_data/general/classif_general_query_dataset.json"
		msg = get_sql(message, "general", ner_dataset, model_save, model_file, dump, sql_dataset)
		return msg

	elif (label == "specific"):
		ner_dataset = "backend/training_data/specific/ner_specific_query_dataset.txt"
		model_file = "backend/trained_data/specific/specific_tflearn_logs"
		model_save = "backend/trained_data/specific/specific_model.tflearn"
		dump = "backend/trained_data/specific/specific_trained_data"
		sql_dataset = "backend/training_data/specific/classif_specific_query_dataset.json"
		msg = get_sql(message, "specific", ner_dataset, model_save, model_file, dump, sql_dataset)
		return msg

	else:
		return "Repeat your query"
		