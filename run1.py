
import pandas as pd
from operator import itemgetter
from nltk.tokenize import regexp_tokenize
from nltk.corpus import stopwords
import nltk
import math
import numpy as np

doc=[]

data_list=[]

index_doc=[]
index_doc2=[]

indexed_list1=[]


vsm_word2=[]
k=0

class List:
    class Node:
        def __init__(self, doc,dtf): #node는 doc_number,dtf link로 구성
            self.doc = doc
            self.dtf=dtf
            self.next = None

    def __init__(self,term): #head는 term,freq,link로 구성
        self.head = None
        self.term=term
        self.freq = 0

    def freq(self):
        return self.freq

    def term(self):
        return self.term

    def add(self,doc,dtf):
        p=self.head
        if p==None:
            self.head=self.Node(doc,dtf)
        else:
            while (p.next != None):
                p=p.next
            p.next = self.Node(doc,dtf)
        self.freq += 1

    def print_list(self): # doc_number를 출력하기 위한 함수
        p=self.head
        res=[]
        while p is not None:
            res.append(p.doc)
            p=p.next
        return res


def token_(data): #토큰화 , doc_set (

    stop_words = set(stopwords.words('english'))
    str_tmp=data.iloc[0]['artist']
    doc_set = []
    for i in range(len(data)):
        if str_tmp!=data.iloc[i]['artist']:
            doc.append(doc_set)
            doc_set=[]
            str_tmp = data.iloc[i]['artist']

        temp = data.iloc[i]['lyrics']
        temp = temp.lower()
        list = regexp_tokenize(temp, "[a-z]['a-z]*")

        result = []
        for w in list:
            if w not in stop_words:
                result.append(w)

        doc_set.append([data.iloc[i]['artist'],data.iloc[i]['song'] , result])

    doc.append(doc_set)
    return doc

def listing(index): #LINKED LIST head:term,doc_freq // node: doc_num, freq in doc_num
    list_set=[]

    tmp_t=index[0][0]
    tmp_d=index[0][1]
    cnt=1
    for i in range(1,len(index)):
        tmp_term=index[i][0]
        tmp_doc=index[i][1]

        if(tmp_term==tmp_t and tmp_doc==tmp_d):
           cnt+=1
        else:
            list_set.append([tmp_t,tmp_d,cnt])
            cnt=1
        tmp_t=tmp_term
        tmp_d=tmp_doc
    list_set.append([tmp_t, tmp_d, cnt])

    list_all=[]
    term=list_set[0][0]
    list=List(term)
    list.add(list_set[0][1],list_set[0][2])
    for i in range(1,len(list_set)):
        if(term!=list_set[i][0]):
            list_all.append(list)
            list=List(list_set[i][0])
        list.add(list_set[i][1],list_set[i][2])
        term=list_set[i][0]
    list_all.append(list)

    return list_all

def indexing(idx):  #vsm
    vsm_word1 = []
    for i in range(len(doc[idx])):
        for j in range(len(doc[idx][i][2])):
            index_doc.append([doc[idx][i][2][j],i])

    index_doc.sort(key=itemgetter(0))

    indexed_list1=listing(index_doc)

    for i in range(len(indexed_list1)):  # 각 단어별 weight 계산 단어 1개
        vsm_word1.append([0 for j in range(len(doc[idx]) + 1)])
        vsm_word1[i][0] = indexed_list1[i].term
        p = indexed_list1[i].head
        while (p != None):
            w = (1 + math.log2(p.dtf)) * math.log2(len(doc[idx]) / indexed_list1[i].freq)
            vsm_word1[i][p.doc + 1] = float(w)
            p = p.next

    word_list = []

    for j in range(len(doc[idx])):
        list_s = []
        for i in range(len(vsm_word1)):
            list_s.append([vsm_word1[i][0], vsm_word1[i][j]])
        list_s.sort(key=itemgetter(1), reverse=True)
        for i in range(10):
            word_list.append(list_s[i][0])
    word_list.sort()

    label = []
    label.append('term')
    for i in range(len(doc[idx])):
        label.append(doc[idx][i][1])
    df = pd.DataFrame.from_records(vsm_word1, columns=label)
    sum = []

    print(df)



data=pd.read_csv("mylyrics00.csv")

doc=token_(data)
indexing(0)
