# main filter file
import string
import os
from corpus import Corpus
from trainingcorpus import TrainingCorpus
from testingcorpus import TestingCorpus
from collections import defaultdict

MAX_WORD_LENGTH = 100 # the longest acceptable word would have about this length

class MyFilter():
    def __init__(self):
        self.corpus = None
        self.train_files = None
        self.train_spam_words = defaultdict(int)
        self.train_ham_words = defaultdict(int)
        self.spam_words_num = 0
        self.ham_words_num = 0
        self.spam_files_num = 0
        self.ham_files_num = 0

    def train(self, train_corpus_dir):
        self.corpus = TrainingCorpus(train_corpus_dir, MAX_WORD_LENGTH)

        (self.spam_words, self.ham_words, self.spam_words_num, self.ham_words_num, self.spam_files_num, self.ham_files_num) = self.corpus.create_train_dictionaries()
        return

    def test(self, test_corpus_dir):
        self.corpus = TestingCorpus(test_corpus_dir, self.spam_words, self.ham_words, self.spam_words_num, self.ham_words_num, self.spam_files_num, self.ham_files_num, MAX_WORD_LENGTH)
        
        self.test_files = self.corpus.emails()

        prediction_path = os.path.join(test_corpus_dir, '!prediction.txt')
        prediction_file = open(prediction_path, 'w', encoding='utf-8')
        
        for file_name in self.test_files.keys():
            is_spam = self.corpus.test_mail(file_name)
            if is_spam == True:
                prediction_file.writelines(f'{file_name} SPAM\n')
            else:
                prediction_file.write(f'{file_name} OK\n')

        prediction_file.close()
            
x = MyFilter()
x.train('data/1')
x.test('data/2')