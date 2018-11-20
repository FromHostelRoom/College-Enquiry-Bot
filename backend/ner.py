import nltk
import collections
import sys
from nltk.tag import tnt
from backend.query_generation import form_query
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from backend.search_college import get_college_name
from backend.query_execution import execute_general_query
from backend.query_execution import execute_specific_query

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


def get_ner(message, dataset):
    tnt_pos_tagger = train_ner(dataset)
    text = remove_stopwords(message)
    a = tnt_pos_tagger.tag(text)
    print(a)
    
    val=collections.Counter([y for (x,y) in a])
    l = dict(val)
    tag_set = [k for k,v in l.items() if v > 1 and k != "NONE"]
    new_word = ""
    for k in tag_set:
      for (w,t) in list(a):
        if t == k:
          new_word += " "+(w)
          a.remove((w,t))
      new_word = new_word.strip() 
      a = a + [(new_word,t)]
     
    a = dict(a)
    a = {v: k for k, v in a.items()}
    print(a)

    tags = [k for k,v in a.items() if (k != "Unk" and k!= "NONE")]        
    tag_string = ' '.join(tags)
    print(tag_string)
    return a, tag_string


def get_sql(message, query_type, ner_dataset, model_save, model_file, dump, sql_dataset):
    gn = get_ner(message, ner_dataset)
    a = gn[0]
    tag_string = gn[1]

    raw_sql = form_query(tag_string, sql_dataset, model_file, model_save, dump, query_type)
    print("Original Query ",raw_sql)
    
    if query_type == "general":
        for k,v in a.items():
            if k in raw_sql:
                raw_sql = raw_sql.replace(k,v)
        print("Actual Query: ",raw_sql)
        return (execute_general_query(raw_sql))

    if query_type == "specific":
        for k,v in a.items():
            rs = raw_sql[0]
            if k in raw_sql[0]:
                raw_sql[0] = raw_sql[0].replace(k,"'"+v+"'")
        college = a["Unk"]
        col_name = get_college_name(college)
        col_name = ''.join(col_name)
        print(col_name)
        raw_sql[0] = raw_sql[0].replace('COLLEGE',"'"+col_name+"'")
        raw_sql[2] = raw_sql[2].replace('COLLEGE',"'"+col_name+"'")
        print("Actual Query: ",raw_sql[0])
        return(execute_specific_query(raw_sql))
    

    