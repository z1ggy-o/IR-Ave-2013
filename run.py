from linkedlist import List
import pandas as pd
from operator import itemgetter
from nltk.tokenize import regexp_tokenize
from nltk.stem import PorterStemmer
import math
import numpy as np
data=pd.read_csv("lyrics.csv")
data.dropna(how='any')

doc_set=[]

data_list=[]

index_doc1=[]
index_doc2=[]

indexed_list1=[]
indexed_list2=[]
vsm_word1=[]
vsm_word2=[]
k=0
def token_(): #토큰화 , doc_set (
    for i in range(0,100):
        list1 = []
        temp = data.iloc[i]['lyrics']
        temp = temp.lower()
        list = regexp_tokenize(temp, "[a-z]['a-z]*")
        for j in range(len(list)-1):
            list1.append(list[j]+" "+list[j+1])

        doc_set.append([data.iloc[i]['song'], list,list1])


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

def indexing():
    for i in range(len(doc_set)):
        for j in range(len(doc_set[i][1])):
            index_doc1.append([doc_set[i][1][j],i])

        for j in range(len(doc_set[i][2])):
            index_doc2.append([doc_set[i][2][j],i])

    index_doc1.sort(key=itemgetter(0))
    index_doc2.sort(key=itemgetter(0))

    indexed_list1=listing(index_doc1)
    indexed_list2=listing(index_doc2)


    for i in range(len(indexed_list1)):  # 각 단어별 weight 계산 단어 1개
        vsm_word1.append([0 for j in range(len(doc_set)+1)])
        vsm_word1[i][0] = indexed_list1[i].term
        p = indexed_list1[i].head
        while (p != None):
            w = (1+math.log2(p.dtf)) * math.log2(len(doc_set) / indexed_list1[i].freq)
            vsm_word1[i][p.doc+1] = w
            p = p.next

    for i in range(len(indexed_list2)):  # 각 단어별 weight 계산 단어 2개
        vsm_word2.append([0 for j in range(len(doc_set) + 1)])
        vsm_word2[i][0] = indexed_list2[i].term
        p = indexed_list2[i].head
        while (p != None):
            w = (1 + math.log2(p.dtf)) * math.log2(len(doc_set) / indexed_list2[i].freq)
            vsm_word2[i][p.doc + 1] = w
            p = p.next



def lsa_model(str):
    str=str.lower()
    list=regexp_tokenize(str, "[a-z]['a-z]*")
    list2=[]
    for i in range(len(list)-1):
        list2.append(list[i]+" "+list[i+1])

    vsm=np.zeros((len(vsm_word1),len(doc_set)))
    query=np.zeros((len(vsm_word1),1))

    for i in range(len(vsm_word1)): #vsm
        for j in range(len(doc_set)):
            vsm[i][j]=vsm_word1[i][j+1]
        for l in range(len(list)):
            if vsm_word1[i][0] == list[l]:
                query[i][0] = query[i][0] + 1

    print("Vector space model(word by num_doc) :")
    print(vsm)
    print("Query(word by num_doc) :")
    print(query)

    U, S, V_T = np.linalg.svd(vsm, full_matrices=True) #SVD 적용 해서 vsm을 u,s,v_T 로 분해해
    print("matrix U(num_doc by num_doc) : ")
    print(U)
    print("maxtrix S : ")
    print(S)
    print("matrix V_T(num_doc by num_doc) : ")
    print(V_T)

    U_k=np.zeros((len(U),k))
    S_k=np.zeros((k,k))
    V_T_k=np.zeros((k,len(doc_set)))


    for i in range(len(U)):
        for j in range(0,k):
            U_k[i][j]=U[i][j]
    for i in range(0,k):
        S_k[i][i]=S[i]
    for i in range(0,k):
        for j in range(0,len(doc_set)):
            V_T_k[i][j]=V_T[i][j]

    S_k_inv=np.linalg.inv(S_k)
    q=np.dot(query.T,np.dot(U_k,S_k_inv))

    V_k=V_T_k.T

    sim=np.zeros(len(doc_set))

    for i in range((len(V_k))): #cos similarity 계산
        temp_q_1=q[0][0]*V_k[i][0]+q[0][1]*V_k[i][1]
        temp_q_2=math.sqrt(pow(V_k[i][0],2)+pow(V_k[i][1],2))
        temp_q_3=math.sqrt(pow(q[0][0],2)+pow(q[0][1],2))
        sim[i]=temp_q_1/(temp_q_2*temp_q_3)

    result=[]
    for i in range(0,len(doc_set)):
        result.append([doc_set[i][0],sim[i],i])
    result.sort(key=itemgetter(1),reverse=True) #similarity 배열 내림차순 정렬

    print("결과값 :")
    for i in range(0,10):
        print("song : ",result[i][0],"// similarity : ",result[i][1])

    query2 = np.zeros((len(vsm_word2), 1))
    vsm_2 = np.zeros((len(vsm_word2), 10))

    for i in range(len(vsm_word2)):  # vsm
        for j in range(10):
            vsm_2[i][j] = vsm_word2[i][result[j][2]+1]
        for l in range(len(list2)):
            if vsm_word2[i][0] == list2[l]:
                query2[i][0] = query2[i][0] + 1


    U_2, S_2, V_T_2 = np.linalg.svd(vsm_2, full_matrices=False)  # SVD 적용 해서 vsm을 u,s,v_T 로 분해해


    print("matrix U(num_doc by num_doc) : ")
    print(U_2)
    print("maxtrix S : ")
    print(S_2)
    print("matrix V_T(num_doc by num_doc) : ")
    print(V_T_2)
    U_k_2 = np.zeros((len(U_2), k))
    S_k_2 = np.zeros((k, k))
    V_T_k_2 = np.zeros((k, 10))

    for i in range(len(U_2)):  # 입력받은 k 값에 대해 dimension 축소
        for j in range(0, k):
            U_k_2[i][j] = U_2[i][j]
    for i in range(0, k):
        S_k_2[i][i] = S_2[i]
    for i in range(0, k):
        for j in range(0, 10):
            V_T_k_2[i][j] = V_T_2[i][j]

    S_k_inv_2 = np.linalg.inv(S_k_2)
    q_2 = np.dot(query2.T, np.dot(U_k_2, S_k_inv_2))

    V_k_2 = V_T_k_2.T

    sim_2 = np.zeros(10)

    for i in range((len(V_k_2))):  # cos similarity 계산
        temp_q_1 = q_2[0][0] * V_k_2[i][0] + q_2[0][1] * V_k_2[i][1]
        temp_q_2 = math.sqrt(pow(V_k_2[i][0], 2) + pow(V_k_2[i][1], 2))
        temp_q_3 = math.sqrt(pow(q_2[0][0], 2) + pow(q_2[0][1], 2))
        if temp_q_2 * temp_q_3 == 0:
            sim_2[i]=0
        else:
            sim_2[i] = temp_q_1 / (temp_q_2 * temp_q_3)

    result_2 = []
    for i in range(0, 10):
        result_2.append([doc_set[result[i][2]][0], sim_2[i]])
    result_2.sort(key=itemgetter(1), reverse=True)  # similarity 배열 내림차순 정렬

    print("결과값 :")
    for i in range(0, 10):
        print("song : ", result_2[i][0], "// similarity : ", result_2[i][1])


data=pd.read_csv("lyrics.csv")
data.dropna(how='any')
token_()
indexing()
print("검색어 입력 : ")
input_str=input()
k=2
##find_rank(input_str)
lsa_model(input_str)
