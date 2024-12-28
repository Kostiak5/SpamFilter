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
        counter = 0

        prediction_path = os.path.join(test_corpus_dir, '!prediction.txt')
        prediction_file = open(prediction_path, 'w', encoding='utf-8')
        for file_name in self.test_files.keys():
            is_spam = self.corpus.test_mail(file_name)
            if is_spam == True:
                prediction_file.writelines(f'{file_name} SPAM\n')
            else:
                prediction_file.write(f'{file_name} OK\n')

        prediction_file.close()
        #self.corpus.test_mail('0299.9d0b292172cb787eb2ed9e8855222edd')
        """
            if counter == 1:
                break
                
            counter += 1
            self.corpus.test_mail('00549.703d3fc9f56814c467616f8aac31d22d')
        self.corpus.test_mail('0310.23036f6ae05720b052b73117b6ecb957')
        self.corpus.test_mail('0387.38b98a83546245da45d8aeb3ff4b1098')
        self.corpus.test_mail('00655.db3781e31126e0d5dc09de092da8a2f0')
        self.corpus.test_mail('00807.8abdd26ba778758f5e46b84a54ac62f4')
        self.corpus.test_mail('00097.90200a177414673b08df827239a0b9dc')
        self.corpus.test_mail('00240.6430542510c59bcb5e4cca0112eff3ac')
        self.corpus.test_mail('01345.436954c32bbf82773e33853ac26ef881')
        self.corpus.test_mail('0255.42a6feb4435a0a68929075c0926f085d')
        self.corpus.test_mail('00154.b6c448ccff434e2dbe2c7c200a36aa31')
        self.corpus.test_mail('0210.aa264fefcd8fe85855dc2f400c4683e7')
        self.corpus.test_mail('00403.b1daf6c6c299354f3b46c5fca2296aee')
        """
            
x = MyFilter()
x.train('data/1')
x.test('data/2')