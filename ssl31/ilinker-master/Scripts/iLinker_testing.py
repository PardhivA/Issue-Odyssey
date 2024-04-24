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

    
def getText(repo,issue_id,cur):
    try:
        query = "select title,body,user from issues where repo=\"%s\" and issue_id=%s"%(repo,issue_id)
        cur.execute(query)
        data = cur.fetchone()
        if data != None:
            return data[0]+" "+data[1],data[2]
    except pymysql.Error as e:
        print ("Mysql Error!", e);     


def getActualLinks(repo,issue_id,cur):
    actual_links = []
    try:
        query = "select distinct(issue_id) from issue_events_cross where repo=\"%s\" and link_issue_id=%s "\
                "and repo=link_repo and issue_id<link_issue_id "%(repo,issue_id)
        cur.execute(query)
        data = cur.fetchone()
        while data != None:
            actual_links.append(data[0])
            data = cur.fetchone()
    except pymysql.Error as e:
        print ("Mysql Error!", e);
    return actual_links


def doc2vecScore(model,issue_id,n,docLabels,index):
    result = []
    infer_vector = model.docvecs["SENT_%s"%issue_id]
    for label in docLabels:
        sim = cosine_similarity(infer_vector.reshape(1, -1),model.docvecs["SENT_%s"%label].reshape(1, -1))
        result.append([label,float(sim)+1]) 
    return result

def tfIdfScore(issue_id,model_index,model,text,dict,n,docLabels,index):
    query_doc = list(preprocessing(text))
    query_doc_bow = dict.doc2bow(query_doc)
    query_tfidf = model[query_doc_bow]
    sims = model_index[query_tfidf]
    result = []   
    for sim in enumerate(sims):
        sim = list(sim)
        result.append([docLabels[int(sim[0])],sim[1]+1]) 
    return result

def getDocVector(text,model):
    doc = list(preprocessing(text))
    vectors = []
    for word in doc:
        try:
            vectors.append(model.wv[word])
        except KeyError as e:
            continue
    result = np.array(vectors)
    n = len(vectors)
    m = 200
    result_new = result.sum(axis=0)
    vector = []
    try:
        for x in result_new:
            vector.append(x/n)
    except TypeError as e:
        for i in range(m):
            vector.append(0.0)
    return vector

def word2vecScore(index,model,docLabels,vectors,n):
    query_vec = vectors[index]
    sims = model.wv.cosine_similarities(query_vec,vectors)
    result = []
    for id in range(n):
        result.append([docLabels[id],sims[id]+1]) 
    return result

def removeAftIssues(scores,issue_id,k):
    temp = []
    for score in scores:
        if score[0]<issue_id:
            temp.append(score)
    scores_final = sortFunc(temp)
    result = []
    for score_f in scores_final:
        result.append(int(score_f[0]))
    if len(result)<10:
        n = 10-len(result)
        for i in range(n):
            result.append(0)
    return result[0:k]


def combineScores(scores_d2c,scores_tf,scores_w2c,n):
    result = []
    for id in range(n):
        value = scores_d2c[id][1]+scores_tf[id][1]+scores_w2c[id][1]
        result.append([scores_tf[id][0],value])
    return result

def sortFunc(result):
    for i in range(len(result)):
        for j in range(i,len(result)):
            if result[i][1]<result[j][1]:
                temp = result[i]
                result[i] = result[j]
                result[j] = temp
    return result
    
def testData(repo,docLabels,docData):
    conn = pymysql.connect(host='localhost',user='root',passwd='',db='issues')
    cur = conn.cursor()
    conn_1 = pymysql.connect(host='localhost',user='root',passwd='',db='issues')
    cur_1 = conn_1.cursor()
    conn_2 = pymysql.connect(host='localhost',user='root',passwd='',db='issues')
    cur_2 = conn_2.cursor()
    link_issues = []
    k = 10
    total_result=[0,0,0,0,0,0,0,0,0]
    tf_result = [0,0,0,0,0,0,0,0,0]
    w2c_result = [0,0,0,0,0,0,0,0,0]
    d2c_result = [0,0,0,0,0,0,0,0,0]
    tf_w2c_result = [0,0,0,0,0,0,0,0,0]
    tf_d2c_result = [0,0,0,0,0,0,0,0,0]
    w2c_d2c_result = [0,0,0,0,0,0,0,0,0]
    n = len(docLabels)
    model_d2c = gensim.models.Doc2Vec.load('%s_d2c.model'%repo.split("/")[0])
    model_w2c = gensim.models.Word2Vec.load('%s_w2c.model'%repo.split("/")[0])
    tfidf_dict =  gensim.corpora.Dictionary.load('%s_tfidf.dict'%repo.split("/")[0])
    tfidf_model = gensim.models.TfidfModel.load('%s_tfidf.model'%repo.split("/")[0])
    tfidf_corpus = gensim.corpora.MmCorpus('%s_tfidf.corpus'%repo.split("/")[0])
    corpus_tfidf = tfidf_model[tfidf_corpus]
    model_index = gensim.similarities.MatrixSimilarity(corpus_tfidf)
    vectors = []
    for doc in docData:
        vectors.append(getDocVector(doc,model_w2c))
    try:
        query = "select distinct(link_issue_id) from issue_events_cross "\
                "where repo=\"%s\" and repo=link_repo and issue_id<link_issue_id "\
                "and link_issue_id in (select issue_id from issues where repo=\"%s\" and state=\"closed\")"%(repo,repo)
        cur.execute(query)
        data = cur.fetchone()
        while data != None:
            issue_id = data[0]
            link_issues.append(issue_id)
            text,user = getText(repo,issue_id,cur_1)
            actual_links = getActualLinks(repo,issue_id,cur_2)
            index = docLabels.index(issue_id)
            scores_w2c = word2vecScore(index,model_w2c,docLabels,vectors,n)
            scores_d2c = doc2vecScore(model_d2c,issue_id,n,docLabels,index)
            scores_tf = tfIdfScore(issue_id,model_index,tfidf_model,text,tfidf_dict,n,docLabels,index)
            #overall
            scores_final = combineScores(scores_d2c,scores_tf,scores_w2c,n)
            predicts_overall = removeAftIssues(scores_final,issue_id,10)
            total_result = calculateValue(issue_id,predicts_overall,actual_links,total_result)  
            #tfidf
            tf_temp = scores_tf
            predicts_tf = removeAftIssues(tf_temp,issue_id,10)
            tf_result = calculateValue(issue_id,predicts_tf,actual_links,tf_result)
            #w2c
            w2c_temp = scores_w2c
            predicts_w = removeAftIssues(w2c_temp,issue_id,10)
            w2c_result = calculateValue(issue_id,predicts_w,actual_links,w2c_result)
            #d2c
            d2c_temp = scores_d2c
            predicts_d = removeAftIssues(d2c_temp,issue_id,10)
            d2c_result = calculateValue(issue_id,predicts_d,actual_links,d2c_result)     
            data = cur.fetchone()
    except pymysql.Error as e:
        print ("Mysql Error!", e);
    cur.close()
    conn.close()
    cur_1.close()
    conn_1.close()
    cur_2.close()
    conn_2.close()
    base_count = len(link_issues)
    print("Total linked issues:",base_count)
    displayResult(base_count,total_result,"Our approach")
    displayResult(base_count,tf_result,"TF-IDF")
    displayResult(base_count,w2c_result,"W2C")
    displayResult(base_count,d2c_result,"D2C")

def displayResult(count,result,approach):
    print("============================")
    print("%s:"%approach)
    print("Top-1:")
    print("Aimed count:", result[0])
    print("Recall@1:",float(result[0])/count)
    print("Top-5:")
    print("Aimed count:", result[3])
    print("Recall@5:",float(result[3])/count)
    print("Top-10:")
    print("Aimed count:", result[6])
    print("Recall@10:",float(result[6])/count)
    print("MAP:",(result[1]+result[4]+result[7])/(3*count))
    print("MRR:",(result[2]+result[5]+result[8])/(3*count))

def calculateValue(issue_id,predicts,actual_links,result):
    scores_final_10 = predicts
    scores_final_5  = scores_final_10[0:5] 
    scores_final_1  = scores_final_10[0:1] 
    result_1 = [] 
    result_5 = [] 
    result_10 = [] 
    #top-1
    for score_1 in scores_final_1:
        if score_1 in actual_links:
            result_1.append(score_1)
    num_1 = len(result_1)
    if num_1 > 0:
        result[0] = result[0]+1
        result[1] = result[1] + float(num_1) 
        result[2] = result[2] + 1.0/(scores_final_1.index(result_1[0])+1) 
    #top-5
    for score_5 in scores_final_5:
        if score_5 in actual_links:
            result_5.append(score_5)
    num_5 = len(result_5)
    if num_5 > 0:
        result[3] = result[3]+1
        result[4] = result[4] + float(num_5)/5
        result[5] = result[5] + 1.0/(scores_final_5.index(result_5[0])+1) 
    #top-10
    for score_10 in scores_final_10:
        if score_10 in actual_links:
            result_10.append(score_10)
    num_10 = len(result_10)
    if num_10 > 0:
        result[6] = result[6]+1
        result[7] = result[7] + float(num_10)/10  
        result[8] = result[8] + 1.0/(scores_final_10.index(result_10[0])+1) 
    return result
    
def getDocLabels(repo):
    conn = pymysql.connect(host='localhost',user='root',passwd='',db='eco_issues')
    cur = conn.cursor()
    docLabels = []
    docData = []
    try:
        query = "select issue_id,title,body from issues where repo=\"%s\" order by issue_id"%repo
        cur.execute(query)
        data = cur.fetchone()
        while data != None:
            docData.append(data[1]+" "+data[2])
            docLabels.append(data[0])
            data = cur.fetchone()
    except pymysql.Error as e:
        print ("Mysql Error!", e);
    cur.close()
    conn.close()
    return docLabels,docData

if __name__ == '__main__':
    #repo = "request/request"
    repo = "moment/moment"
    docLabels,docData = getDocLabels(repo)
    testData(repo,docLabels,docData)