import os
import string
from corpus import Corpus 
from collections import defaultdict
IS_SPAM = True
IS_HAM = False

class TrainingCorpus(Corpus): 
    def __init__(self, corpus_dir, max_word_length):
        self.corpus = None
        self.corpus_dir = corpus_dir
        self.train_files = None
        self.spam_words = defaultdict(int)
        self.ham_words = defaultdict(int)
        self.spam_words_num = 0
        self.ham_words_num = 0
        self.max_word_length = max_word_length

    """
    def get_class(self, file_name): 
        # vstupem bude název souboru s emailem a výstupem buď kód OK nebo SPAM
        truth_file_path = os.path.join(self.corpus_dir, "1/!truth.txt")
        truth_file = open(truth_file_path, 'r')
        file_names = truth_file.read().split() 
        for line in truth_file:
            split_line = line.split()
            if split_line[1] == 'SPAM':
                self.train_files[split_line[0]][1] = IS_SPAM
            else:
                self.train_files[split_line[0]][1] = IS_HAM
        return
    """

    def split_header_and_contents(self, file):
        header = []
        contents = []
        header_ended = False
        file_lines = file.split('\n')
        
        for line in file_lines:
            if header_ended == False and line == '':
                header_ended = True
            elif header_ended == True:
                contents.append(line)
            else:
                header.append(line)
        #print(contents)        
        return (header, contents)

    def get_truth_data(self): # open truth file and add a SPAM/HAM tag to each record in train_files
        truth_file = open(os.path.join(self.corpus_dir, '!truth.txt'), 'r', encoding='utf-8')
        for line in truth_file:
            split_line = line.split()
            if split_line[1] == 'SPAM':
                self.train_files[split_line[0]][1] = IS_SPAM
            else:
                self.train_files[split_line[0]][1] = IS_HAM
    
    def add_word_to_dict(self, word, is_spam):
        if len(word) <= self.max_word_length and is_spam == True: # if word length is above MAX_WORD_LENGTH, it's more likely to be a link which is, however, mostly unique and therefore useless for filter training
            self.spam_words[word] += 1
            self.spam_words_num += 1
        elif len(word) <= self.max_word_length and is_spam == False:
            self.ham_words[word] += 1
            self.ham_words_num += 1
                
    def gather_used_words(self, text, is_spam): # process used words and put them into ham/spam words dictionaries
        for line in text:
            for word in line.split():
                word = self.normalize_word(word) 
                self.add_word_to_dict(word, is_spam)
                

    def create_train_dictionaries(self):
        counter = 0
        self.train_files = self.emails() # train_files: dictionary, keys: email file names, values: [0] contents of the email file [1] SPAM/HAM tag (SPAM = True, HAM = False)
        self.get_truth_data()
        for file in self.train_files.values():
            (header, contents) = self.split_header_and_contents(file[0]) # split to work with header and contents separately
            counter += 1

            self.gather_used_words(contents, file[1]) # process used words and put them into ham/spam words dictionaries
        
        print("THE Spam")
        print(self.spam_words)
        print("THE Ham")
        print(self.ham_words)
        return (self.spam_words, self.ham_words, self.spam_words_num, self.ham_words_num)
    

