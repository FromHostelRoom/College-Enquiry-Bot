import nltk
from nltk.stem.lancaster import LancasterStemmer
import numpy as np
import tflearn
import tensorflow as tf
import random
import json
import string
import unicodedata
import sys
from backend.query_generation import save_model,load_model,bow
import pickle

tbl = dict.fromkeys(i for i in range(sys.maxunicode)
                    if unicodedata.category(chr(i)).startswith('P'))

stemmer = LancasterStemmer()
data = None


def remove_punctuation(text):
    global tbl
    return text.translate(tbl)


def preprocess_data(file):
    global stemmer, data
    with open(file) as json_data:
        data = json.load(json_data)

    categories = list(data.keys())
    words = []
    docs = []

    for each_category in data.keys():
        for each_sentence in data[each_category]:
            each_sentence = remove_punctuation(each_sentence)
            w = nltk.word_tokenize(each_sentence)
            words.extend(w)
            docs.append((w, each_category))

    words = [stemmer.stem(w.lower()) for w in words]
    words = sorted(list(set(words)))

    return docs,categories,words


def return_label(message):

    model_file = "backend/trained_data/initial/initial_tflearn_logs"
    model_save = "backend/trained_data/initial/initial_model.tflearn"
    dump = "backend/trained_data/initial/initial_trained_data"
    #arr = preprocess_data("backend/training_data/initial_training_data.json")
    #save_model(arr, model_file, model_save, dump)
    file = "backend/training_data/initial_training_data.json"
    with open(file) as json_data:
        data = json.load(json_data)
    
    categories = list(data.keys())
    
    data = pickle.load( open( dump, "rb" ) )
    words = data['words']
    classes = data['classes']
    train_x = data['train_x']
    train_y = data['train_y']
    model = load_model(train_x,train_y, model_file, model_save)
    return categories[np.argmax(model.predict([bow(message,words)]))]

