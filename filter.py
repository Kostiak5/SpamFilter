# main filter file

import os
from corpus import Corpus
from trainingcorpus import TrainingCorpus

class MyFilter():
    def __init__(self):
        self.corpus = None

    def train(self, train_corpus_dir):
        self.corpus = Corpus(train_corpus_dir)
        self.train_files = self.corpus.emails()
        for file in self.train_files:
            print(file)
        return

    #def test():

x = MyFilter()
x.train('data/1')