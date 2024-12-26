# main filter file
import string
import os
from corpus import Corpus
from trainingcorpus import TrainingCorpus
from collections import defaultdict

MAX_WORD_LENGTH = 20 # the longest acceptable word would have about this length

class MyFilter():
    def __init__(self):
        self.corpus = None
        self.train_files = None
        self.train_spam_words = defaultdict(int)
        self.train_ham_words = defaultdict(int)
        self.spam_words_num = 0
        self.ham_words_num = 0

    def train(self, train_corpus_dir):
        self.corpus = TrainingCorpus(train_corpus_dir, MAX_WORD_LENGTH)

        (self.spam_words, self.ham_words, self.spam_files_num, self.ham_files_num) = self.corpus.create_train_dictionaries()
        return

    def test(self, test_corpus_dir):
        self.corpus = TrainingCorpus(test_corpus_dir)
        
        self.test_files = self.corpus.emails()


x = MyFilter()
x.train('data/1')