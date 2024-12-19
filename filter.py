# main filter file

import os
from corpus import Corpus
from trainingcorpus import TrainingCorpus

class MyFilter():
    def __init__(self):
        self.corpus = None

    def split_header_and_contents(self, file):
        header = []
        contents = []
        header_ended = False
        file_lines = file.split('\n')
        for line in file_lines:
            if line == '' and header_ended == False:
                header_ended = True
            elif header_ended == True:
                contents.append(line)
            else:
                header.append(line)
        return (header, contents)
                


    def train(self, train_corpus_dir):
        self.corpus = Corpus(train_corpus_dir)
        self.train_files = self.corpus.emails()
        counter = 0
        for file in self.train_files:
            (header, contents) = self.split_header_and_contents(file)
            counter += 1

        print(counter)
        return

    #def test():

x = MyFilter()
x.train('data/1')