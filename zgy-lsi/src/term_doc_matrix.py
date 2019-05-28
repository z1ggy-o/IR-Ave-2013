"""
ZHU GUANGYU 20165953
"""

import sys
import re
import csv
import math
import numpy as np


class TermDocMatrix:

    punctuation = re.compile(r'[^\w\s\']')
    stopwords = {'a', 'able', 'about', 'across', 'after', 'all', 'almost',
                    'also', 'am', 'among', 'an', 'and', 'any', 'are', 'as', 'at',
                    'be', 'because', 'been', 'but', 'by', 'can', 'cannot', 'could',
                    'dear', 'did', 'do', 'does', 'either', 'else', 'ever', 'every',
                    'for', 'from', 'get', 'got', 'had', 'has', 'have', 'he', 'her',
                    'hers', 'him', 'his', 'how', 'however', 'i', 'if', 'in', 'into',
                    'is', 'it', 'its', 'just', 'least', 'let', 'like', 'likely', 'may',
                    'me', 'might', 'most', 'must', 'my', 'neither', 'no', 'nor',
                    'not', 'of', 'off', 'often', 'on', 'only', 'or', 'other', 'our',
                    'own', 'rather', 'said', 'say', 'says', 'she', 'should', 'since',
                    'so', 'some', 'than', 'that', 'the', 'their', 'them', 'then',
                    'there', 'these', 'they', 'this', 'tis', 'to', 'too', 'twas',
                    'us', 'wants', 'was', 'we', 'were', 'what', 'when', 'where',
                    'which', 'while', 'who', 'whom', 'why', 'will', 'with', 'would',
                    'yet', 'you', 'your'}

    def __init__(self):
        self.docs_list = {}  # Mapping docs_id and docs name
        self.inverted_index = {}  # inverted index: {term: [(doc_id, tf)]}
        self.term_doc_matrix = None
        self.term_row_mapping = {}
        self.num_row = None
        self.num_col = None

    def create_matrix(self):
        self.__indexing()
        self.__create_term_doc_matrix()

    def query_process(self, query):

        query_vector = np.zeros(self.num_row)
        terms = {}

        for term in re.sub(TermDocMatrix.punctuation, ' ', query).split():
            if term not in self.inverted_index:
                continue
            if term not in terms:
                terms[term] = 1
            else:
                terms[term] += 1

        for term, tf in terms.items():
            weight = self.__compute_weight(tf, len(self.inverted_index[term]))
            row = self.term_row_mapping[term]
            query_vector[row] = weight

        return query_vector

    # Create inverted-index
    def __indexing(self):
        """Read script files, 

        Get script list file from command line, read script one by one. Remove
        punctuation and stopwords. Count term frequency and document frequency.
        """

        if len(sys.argv) > 2:
            print('Usage: python search.py file_name')
            exit()
        file_path = sys.argv[1]

        # Build docs list
        doc_id = 0
        with open(file_path, 'r') as docs:
            doc = docs.readline()
            while (doc):
                if doc_id not in self.docs_list:
                    self.docs_list[doc_id] = doc.strip()
                    self.__update_inverted_index(doc, doc_id)
                    doc_id += 1
                doc = docs.readline()

    def __update_inverted_index(self, doc, doc_id):
        '''Create inverted index, count doc vector length

        Read contents form file, remove punctuation and stopwords to get terms.
        Count tf of this doc, then update inverted index.
        '''
        # Count term frequency
        doc_path = '../text/' + doc.strip()
        indices = {}
        with open(doc_path, 'r') as f:
            raw_line = f.readline()
            while(raw_line):
                line = raw_line.strip()
                if (not line):
                    raw_line = f.readline()
                    continue
                for word in re.sub(TermDocMatrix.punctuation, ' ', line).split():
                    word_low = word.lower()
                    if word_low in TermDocMatrix.stopwords:
                        continue
                    elif word_low in indices:
                        indices[word_low] += 1
                    else:
                        indices[word_low] = 1
                raw_line = f.readline()

        # Update inverted_index
        for pair in indices.items():
            term, frequency = pair
            if term in self.inverted_index:
                posting = self.inverted_index[term]
                posting.append((doc_id, frequency))
                self.inverted_index[term] = posting
            else:
                self.inverted_index[term] = [(doc_id, frequency)]

    def __create_term_doc_matrix(self):
        # Create term-docs matrix
        terms = list(self.inverted_index.keys())
        self.num_row = len(terms)
        self.num_col = len(self.docs_list)
        self.term_doc_matrix = np.zeros((self.num_row, self.num_col))

        for i in range(self.num_row):
            self.term_row_mapping[terms[i]] = i

        # Put weight into matrix
        for item in self.inverted_index.items():
            term, posting = item
            df = len(posting)
            row_num = self.term_row_mapping[term]
            for pair in posting:
                id, tf = pair
                weight = self.__compute_weight(tf, df)
                self.term_doc_matrix[row_num][id] = weight

    def __compute_weight(self, tf, df):

        num_of_docs = len(self.docs_list)
        idf = math.log(num_of_docs/df)

        tf_normalized = 1 + math.log(tf)

        weight = tf_normalized * idf

        return weight
