import nltk
import collections
import sys
from nltk.tag import tnt
from backend.query_generation import form_query
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from backend.search_college import get_college_name
from backend.query_execution import execute_query

def untag(tagged_sentence):
    return [w for w, t in tagged_sentence]
 
def transform_to_dataset(tagged_sentences):
    ts =[]
    annotated_sentences = tagged_sentences.split('\n\n')
    for annotated_sentence in annotated_sentences:
        annotated_tokens = [nltk.tag.str2tuple(t) for t in annotated_sentence.split()]
        ts.append(annotated_tokens)
    return ts

def train_ner(training_dataset):
    f = open(training_dataset,"r")
    tagged_sentences = f.read()

    X = transform_to_dataset(tagged_sentences)
    cutoff = int(.75 * len(X))
    training_sents = X[:cutoff]
    test_sents = X[cutoff:]

    tnt_pos_tagger = tnt.TnT()
    tnt_pos_tagger.train(training_sents)
    tnt_pos_tagger.evaluate(test_sents)
    return tnt_pos_tagger

def remove_stopwords(raw_text):
    #stopwords.append('colleges')
    stop_words = set(stopwords.words('english'))
    raw_text = raw_text.lower() 
    word_tokens = word_tokenize(raw_text) 
    query = [w for w in word_tokens if not w in stop_words] 
    return query


def get_ner(message, dataset, query_type):
    tnt_pos_tagger = train_ner(dataset)
    text = remove_stopwords(message)
    a = tnt_pos_tagger.tag(text)
    print(a)
    if query_type == "general":
        tags = [t for w,t in a if t != "NONE"]

    if query_type == "specific":
        tags = [t for w,t in a if t != "Unk"]
    
    tag_string = ' '.join(tags)
    print(tag_string)
    return a, tag_string


def get_sql(message, query_type, ner_dataset, model_save, model_file, dump, sql_dataset):
    gn = get_ner(message, ner_dataset, query_type)
    a = gn[0]
    tag_string = gn[1]

    raw_sql = form_query(tag_string, sql_dataset, model_file, model_save, dump)
    print("Original Query ",raw_sql)
    
    for word,tag in a:
        if tag in raw_sql:
            raw_sql = raw_sql.replace(tag,"'"+word+"'")
            print("Actual query: ",raw_sql)

    if query_type == "specific":
        college = [w for w,t in a if t=="Unk"]
        col_name = ' '.join(college)
        col_name = get_college_name(col_name)
        col_name = ''.join(col_name)
        raw_sql = raw_sql.replace('COLLEGE',"'"+col_name+"'")
    
    sql = raw_sql
    print("Actual Query: ",sql)
    return sql