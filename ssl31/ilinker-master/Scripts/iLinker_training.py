import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import gensim
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import re
from gensim import utils
from gensim.models.doc2vec import TaggedDocument
from gensim.models import Doc2Vec
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from gensim.models import TfidfModel
from gensim.corpora import Dictionary
import pymysql
from sklearn.feature_extraction.text import HashingVectorizer  
from nltk.tokenize import word_tokenize
from nltk.stem.lancaster import LancasterStemmer
import nltk.data
from sklearn.metrics.pairwise import cosine_similarity
import time

def preprocessing(document):
    document_tokenized = [word.lower() for word in word_tokenize(document)]
    english_stopwords = stopwords.words('english')
    document_stopwords = [word for word in document_tokenized if word not in english_stopwords]
    english_punctuations = [":",".","\n","/","@", "\\","*","=","^",";","_","|",
                               '"',"' "," '","-",
                               "(",")",",",">","<",
                               "!","?","[","]","+",
                               "&","%","$","#","~","{","}"]
    document_filtered = [word for word in document_stopwords if not word in english_punctuations]
    st = LancasterStemmer()
    document_stem = [st.stem(word) for word in document_filtered]
    return document_stem

class read_corpus(object):
    def __init__(self, doc_list, labels_list, tags_list, types_list):
       self.labels_list = labels_list
       self.doc_list = doc_list
       self.tags_list = tags_list
       self.types_list = types_list
    def __iter__(self):
        for idx, doc in enumerate(self.doc_list):
            yield TaggedDocument(words=preprocessing(doc),tags=[self.tags_list[idx],self.types_list[idx],"SENT_%s"%self.labels_list[idx]])

def doc2vec(repo):
    conn = pymysql.connect(host='localhost',user='root',passwd='',db='issues')
    cur = conn.cursor()
    docLabels = []
    docData = []
    docTags = []
    docTypes = []
    try:
        query = "select issue_id,title,body,user,type from issues where repo=\"%s\""%repo
        cur.execute(query)
        data = cur.fetchone()
        while data != None:
            docLabels.append(data[0])
            docData.append(data[1]+" "+data[2])
            docTags.append(data[3])
            if data[4]==1:
                docTypes.append("PR")
            else:
                docTypes.append("Issue")
            data = cur.fetchone()
    except pymysql.Error as e:
        print ("Mysql Error!", e);
    cur.close()
    conn.close()
    print("Loading data done!")
    it = list(read_corpus(docData, docLabels, docTags, docTypes))
    model = gensim.models.Doc2Vec(dm=0,size=200,min_count=2,epochs=100,window=5,alpha=0.025) # use fixed learning rate
    model.build_vocab(it)
    model.train(it,total_examples = model.corpus_count,epochs = model.epochs)
    model.save("%s_d2c.model"%repo.split("/")[0])
    print("Building model done!")
    
def word2vec(repo):
    conn = pymysql.connect(host='localhost',user='root',passwd='',db='issues')
    cur = conn.cursor()
    docLabels = []
    docData = []
    try:
        query = "select issue_id,title,body from issues where repo=\"%s\" order by issue_id"%repo
        cur.execute(query)
        data = cur.fetchone()
        while data != None:
            docLabels.append(data[0])
            docData.append(preprocessing(data[1]+" "+data[2]))
            data = cur.fetchone()
    except pymysql.Error as e:
        print ("Mysql Error!", e);
    cur.close()
    conn.close()
    print("Loading data done!")
    model = gensim.models.Word2Vec(sg=1,size=200,min_count=2,window=5,alpha=0.025) # use fixed learning rate
    model.build_vocab(docData)
    model.train(docData,total_examples = model.corpus_count,epochs = 100)
    model.save("%s_w2c.model"%repo.split("/")[0])
    print("Building model done!")
    return docLabels

def tfIdf(repo):
    conn = pymysql.connect(host='localhost',user='root',passwd='',db='issues')
    cur = conn.cursor()
    docLabels = []
    docData = []
    try:
        query = "select issue_id,title,body from issues where repo=\"%s\" order by issue_id"%repo
        cur.execute(query)
        data = cur.fetchone()
        while data != None:
            docLabels.append(str(data[0]))
            docData.append(preprocessing(data[1]+" "+data[2]))
            data = cur.fetchone()
    except pymysql.Error as e:
        print ("Mysql Error!", e);
    cur.close()
    conn.close()
    print("Loading data done!")
    dictionary = gensim.corpora.Dictionary(docData)
    corpus = [dictionary.doc2bow(text) for text in docData]
    model = gensim.models.TfidfModel(corpus)
    dictionary.save("%s_tfidf.dict"%repo.split("/")[0])
    model.save("%s_tfidf.model"%repo.split("/")[0])
    gensim.corpora.MmCorpus.serialize("%s_tfidf.corpus"%repo.split("/")[0],corpus)
    print("Building model done!")
    return docLabels
   

if __name__ == '__main__':
    #repo = "request/request"
    repo = "moment/moment"
    tfIdf(repo)
    doc2vec(repo)
    word2vec(repo)
