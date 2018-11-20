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
from textblob.classifiers import NaiveBayesClassifier
from backend.training_data.dataset import train

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
    cl = NaiveBayesClassifier(train)
    print("RUNNING...")
    return(cl.classify(message))

