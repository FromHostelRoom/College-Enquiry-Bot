import nltk
from nltk.stem.lancaster import LancasterStemmer
import numpy as np
import tflearn
import tensorflow as tf
import random
import json
import pickle
from nltk.corpus import stopwords

stemmer = LancasterStemmer()

def preprocess_text(file):
	with open(file) as json_data:
	    intents = json.load(json_data)

	words = []
	classes = []
	documents = []
	ignore_words = ['?']
	stemmer = LancasterStemmer()
	# loop through each sentence in our intents patterns
	for intent in intents['entity_examples']:
	        # tokenize each word in the sentence
	        w = nltk.word_tokenize(intent['text'])
	        # add to our words list
	        words.extend(w)
	        # add to documents in our corpus
	        documents.append((w, intent['intent']))
	        # add to our classes list
	        if intent['intent'] not in classes:
	            classes.append(intent['intent'])

	# stem and lower each word and remove duplicates
	words = [stemmer.stem(w.lower()) for w in words if w not in ignore_words]
	words = sorted(list(set(words)))

	# remove duplicates
	classes = sorted(list(set(classes)))

	return documents,classes,words

def train_data(arr):
	#arr = preprocess_data(file)
	documents = arr[0]
	classes = arr[1]
	words = arr[2]
	# create our training data
	training = []
	output = []
	# create an empty array for our output
	output_empty = [0] * len(classes)

	# training set, bag of words for each sentence
	for doc in documents:
	    # initialize our bag of words
	    bag = []
	    # list of tokenized words for the pattern
	    pattern_words = doc[0]
	    # stem each word
	    pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]
	    # create our bag of words array
	    for w in words:
	        bag.append(1) if w in pattern_words else bag.append(0)

	    # output is a '0' for each tag and '1' for current tag
	    output_row = list(output_empty)
	    output_row[classes.index(doc[1])] = 1

	    training.append([bag, output_row])

	# shuffle our features and turn into np.array
	random.shuffle(training)
	training = np.array(training)

	# create train and test lists
	train_x = list(training[:,0])
	train_y = list(training[:,1])
	return train_x, train_y,classes,words

def save_model(arr,model_file, model_save, dump_file):
	td = train_data(arr)
	train_x = td[0]
	train_y = td[1]
	classes = td[2]
	words = td[3]
	# reset underlying graph data
	tf.reset_default_graph()
	# Build neural network
	net = tflearn.input_data(shape=[None, len(train_x[0])])
	net = tflearn.fully_connected(net, 8)
	net = tflearn.fully_connected(net, 8)
	net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
	net = tflearn.regression(net)

	# Define model and setup tensorboard
	model = tflearn.DNN(net, tensorboard_dir = model_file)
	# Start training (apply gradient descent algorithm)
	model.fit(train_x, train_y, n_epoch=1000, batch_size=8, show_metric=True)
	model.save(model_save)
	pickle.dump( {'words':words, 'classes':classes, 'train_x':train_x, 'train_y':train_y}, open(dump_file, "wb" ) )
	return train_x,train_y

def clean_up_sentence(sentence):
    # tokenize the pattern
    #sentence_words = nltk.word_tokenize(sentence)
    # stem each word
    
    stop_words = set(stopwords.words('english'))
    word_tokens = nltk.word_tokenize(sentence) 
    sentence_words = [w for w in word_tokens if not w in stop_words] 
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details=False):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)

    return(np.array(bag))


ERROR_THRESHOLD = 0.25
def classify(model,words,classes,sentence):
    # generate probabilities from the model
    results = model.predict([bow(sentence, words)])[0]
    # filter out predictions below a threshold
    results = [[i,r] for i,r in enumerate(results) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append((classes[r[0]], r[1]))
    # return tuple of intent and probability
    return return_list

def response(model,words,classes,intents,sentence):
    results = classify(model,words,classes,sentence)
    # if we have a classification then find the matching intent tag
    if results:
        # loop as long as there are matches to process
        while results:
            for i in intents['entity_examples']:
                # find a tag matching the first result
                if i['intent'] == results[0][0]:
                    # a random response from the intent
                    return (i['query'])

         

def load_model(train_x,train_y, model_file, model_save):
	
	tf.reset_default_graph()
		# Build neural network
	net = tflearn.input_data(shape=[None, len(train_x[0])])
	net = tflearn.fully_connected(net, 8)
	net = tflearn.fully_connected(net, 8)
	net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
	net = tflearn.regression(net)

		# Define model and setup tensorboard
	model = tflearn.DNN(net, tensorboard_dir= model_file)
	model.load('./'+model_save)
	return model

def form_query(text,sql_dataset, model_file, model_save, dump):
	#arr = preprocess_text(sql_dataset)
	#save_model(arr, model_file, model_save, dump)
	data = pickle.load( open( dump, "rb" ) )
	words = data['words']
	classes = data['classes']
	train_x = data['train_x']
	train_y = data['train_y']
	model = load_model(train_x,train_y, model_file, model_save)
	with open(sql_dataset) as json_data:
		intents = json.load(json_data)
		
	return (response(model,words,classes,intents,text))
 

#after response function, check for all arguments, if stream, substr, loc defined->add a function to extract loc using gpe and stream and substream using start and end position given in entities.
#optional -> add the new training to json file

