# -*- coding: utf-8 -*-
import numpy as np
import scipy.sparse as sp
import scipy.sparse.sparsetools as sptools
from collections import defaultdict





STOP_WORDS_FILENAME = 'stop_words.txt'

#Class is to index the objects
class Indexable(object):


    def __init__(self,metadata):
        self.words_count = defaultdict(int)

        for word in metadata.split():
            self.words_count[word] += 1


# unique words from indexable data
    def words_generator(self, stop_words):

        for word in self.words_count.keys():
            if word not in stop_words or len(word) > 5:
                yield word

    def count_for_word(self, word):

        return self.words_count[word] if word in self.words_count else 0

# result with tf-idf score
class IndexableResult(object):
 

    def __init__(self, score, indexable):
        self.score = score
        self.indexable = indexable

    def __repr__(self):
        return '<!TFIDF_SCORE!>: %f, <!RESULT!>: %s' % (self.score, self.indexable)


# Class representing tf-idf ranking logic
class TfidfRank(object):


    def __init__(self, stop_words, smoothing=1):
        self.smoothing = smoothing
        self.stop_words = stop_words
        self.vocabulary = {}
        self.tf = []
        self.idf = []
        self.tf_idf_matrix = []

    def build_rank(self, objects):
  
        self.build_vocabulary(objects)

        n_terms = len(self.vocabulary)
        n_docs = len(objects)
        tf = sp.lil_matrix((n_docs, n_terms), dtype=np.dtype(float))

       

        # compute idf
        
        for index, indexable in enumerate(objects):
            for word in indexable.words_generator(self.stop_words):
                word_index_in_vocabulary = self.vocabulary[word]
                doc_word_count = indexable.count_for_word(word)
                tf[index, word_index_in_vocabulary] = doc_word_count
        self.tf = tf.tocsc()

        
        # compute idf with smoothing
        df = np.diff(self.tf.indptr) + self.smoothing
        n_docs_smooth = n_docs + self.smoothing

        # create diagonal matrix to be multiplied with ft
        idf = np.log(float(n_docs_smooth) / df) + 1.0
        self.idf = sp.spdiags(idf, diags=0, m=n_terms, n=n_terms)

        # compute tf-idf
        self.tf_idf_matrix = self.tf * self.idf
        self.tf_idf_matrix = self.tf_idf_matrix.tocsr()

        # compute td-idf normalization
        norm = self.tf_idf_matrix.tocsr(copy=True)
        norm.data **= 2
        norm = norm.sum(axis=1)
        n_nzeros = np.where(norm > 0)
        norm[n_nzeros] = 1.0 / np.sqrt(norm[n_nzeros])
        norm = np.array(norm).T[0]
        sptools.csr_scale_rows(self.tf_idf_matrix.shape[0],
                                      self.tf_idf_matrix.shape[1],
                                      self.tf_idf_matrix.indptr,
                                      self.tf_idf_matrix.indices,
                                      self.tf_idf_matrix.data, norm)
    # Build vocab with indexable object
    def build_vocabulary(self, objects):
  
        vocabulary_index = 0
        for indexable in objects:
            for word in indexable.words_generator(self.stop_words):
                if word not in self.vocabulary:
                    self.vocabulary[word] = vocabulary_index
                    vocabulary_index += 1
    #  compute tfidf score of indexed document
    def compute_rank(self, doc_index, terms):
    
        score = 0
        for term in terms:
            term_index = self.vocabulary[term]
            score += self.tf_idf_matrix[doc_index, term_index]
        return score

# Class to index objects
class Index(object):


    def __init__(self, stop_words):
        self.stop_words = stop_words
        self.term_index = defaultdict(list)

    def build_index(self, objects):

        for position, indexable in enumerate(objects):
            for word in indexable.words_generator(self.stop_words):
                # build dictionary where term is the key and an array
                # of the IDs of indexable object containing the term
                self.term_index[word].append(position)

    def search_terms(self, terms):

        docs_indices = []
        for term_index, term in enumerate(terms):

            # keep only docs that contains all terms
            if term not in self.term_index:
                docs_indices = []
                break

            # compute intersection between results
            
            docs_with_term = self.term_index[term]
            if term_index == 0:
                docs_indices = docs_with_term
            else:
                docs_indices = set(docs_indices) & set(docs_with_term)

        return list(docs_indices)

# search engine for indexable objects
class SearchEngine(object):

    def __init__(self):
        self.objects = []
        self.stop_words = self.load_stop_words()
        self.rank = TfidfRank(self.stop_words)
        self.index = Index(self.stop_words)

#filter stop words
    def load_stop_words(self):

        stop_words = {}
        with open(STOP_WORDS_FILENAME) as stop_words_file:
            for word in stop_words_file:
                stop_words[word.strip()] = True
        return stop_words

# add object to index
    def add_object(self, indexable):
       
        self.objects.append(indexable)

#start search
    def start(self):

        
        self.index.build_index(self.objects)
        self.rank.build_rank(self.objects)

#return indexed doc given query
    def search(self, query, n_results=5):

        terms = query.lower().split()
        docs_indices = self.index.search_terms(terms)
        search_results = []

        for doc_index in docs_indices:
            indexable = self.objects[doc_index]
            doc_score = self.rank.compute_rank(doc_index, terms)
            result = IndexableResult(doc_score, indexable)
            search_results.append(result)
          
        search_results.sort(key=lambda x: x.score, reverse=True)

        return search_results[:n_results]
#Return number of objects already in the index.
    def count(self):

        return len(self.objects)