#-*- coding: utf-8 -*-

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