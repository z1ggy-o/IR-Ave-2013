import numpy as np
import term_doc_matrix as tdm


class LSI:

    def __init__(self, k=None):
        self.k = k
        self.matrix = tdm.TermDocMatrix()

        self.Uk = None
        self.Vkt = None
        self.Sigma_k = None

        self.length_VkT = []

    def create_matrix(self):
        self.matrix.create_matrix()

    def svd(self):
        # Do SVD
        self.__svd_k()

        # Compute length of each column of VkT(document matrix)
        Vk = self.Vkt.transpose()
        for i in range(len(Vk)):
            row = Vk[i]
            length = np.linalg.norm(row)
            self.length_VkT.append(length)

    def search(self, query):
        '''Search query matched documents

        Compute the similarity between query and documents.
        Print out related documents in decrease score order
        '''
        query_vector = self.matrix.query_process(query)

        # Mapping query vector into LSI space
        query_k = query_vector.dot(self.Uk).dot(np.linalg.inv(self.Sigma_k))

        scores = self.__compute_score(query_k)

        sorted_docs = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)

        if (not sorted_docs):
            print(f'\nThere is no relevant document.')
        else:
            print('\nSearch results are: ')
            for doc in sorted_docs:
                print('-> ' + self.matrix.docs_list[doc[0]])
        print()

        print('Scores are:')
        for score in sorted_docs:
            print('%10f: ' % score[1] + str(self.matrix.docs_list[score[0]]))
        print()

    def __compute_score(self, query_k):
        scores = {}
        for i in range(self.matrix.num_col):
            doc_v = self.Vkt[:, i:i+1]
            score = query_k.dot(doc_v) / self.length_VkT[i]
            scores[i] = score

        return scores

    def __svd_k(self):

        u, sigma, vt = np.linalg.svd(self.matrix.term_doc_matrix)

        if not self.k:
            self.k = len(sigma)
        elif self.k > self.matrix.num_col:
            self.k = len(sigma)

        # Truncate matrix, remove zero elements
        self.Sigma_k = np.diag(sigma[:self.k])
        self.Uk = u[:, :self.k]
        self.Vkt = vt[:self.k, :]
