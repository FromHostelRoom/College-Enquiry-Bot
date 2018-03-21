from backend.classify_query import preprocess_data
from backend.query_generation import save_model,preprocess_text


def train_query_classifier():
	model_file = "backend/trained_data/initial/initial_tflearn_logs"
	model_save = "backend/trained_data/initial/initial_model.tflearn"
	dump = "backend/trained_data/initial/initial_trained_data"
	arr = preprocess_data("backend/training_data/initial_training_data.json")
	save_model(arr, model_file, model_save, dump)

def train_general_query_classifier():
	model_file = "backend/trained_data/general/general_tflearn_logs"
	model_save = "backend/trained_data/general/general_model.tflearn"
	dump = "backend/trained_data/general/general_trained_data"
	sql_dataset = "backend/training_data/general/classif_general_query_dataset.json"
	arr = preprocess_text(sql_dataset)
	save_model(arr, model_file, model_save, dump)

def train_specific_query_classifier():
	model_file = "backend/trained_data/specific/specific_tflearn_logs"
	model_save = "backend/trained_data/specific/specific_model.tflearn"
	dump = "backend/trained_data/specific/specific_trained_data"
	sql_dataset = "backend/training_data/specific/classif_specific_query_dataset.json"
	arr = preprocess_text(sql_dataset)
	save_model(arr, model_file, model_save, dump)