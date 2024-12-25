# main filter file
import string
import os
from corpus import Corpus
from trainingcorpus import TrainingCorpus
from collections import defaultdict


COMMON_SPAM_WORDS = ["#1", "100% more", "100% free", "100% satisfied", "additional income", "be your own boss", "best price", "big bucks", "billion", "cash bonus", "cents on the dollar", "consolidate debt", "double your cash", "double your income", "earn extra cash", "earn money", "eliminate bad credit", "extra cash", "extra income", "expect to earn", "fast cash", "financial freedom", "free access", "free consultation", "free gift", "free hosting", "free info", "free investment", "free membership", "free money", "free preview", "free quote", "free trial", "full refund", "get out of debt", "get paid", "giveaway", "guaranteed", "increase sales", "increase traffic", "incredible deal", "lower rates", "lowest price", "make money", "million dollars", "miracle", "money back", "once in a lifetime", "one time", "pennies a day", "potential earnings", "prize", "promise", "pure profit", "risk-free", "satisfaction guaranteed", "save big money", "save up to", "special promotion", "act now", "apply now", "become a member", "call now", "click below", "click here", "get it now", "do it today", "don’t delete", "exclusive deal", "get started now", "important information regarding", "information you requested", "instant", "limited time", "new customers only", "order now", "please read", "see for yourself", "sign up free", "take action", "this won’t last", "urgent", "what are you waiting for?", "while supplies last", "will not believe your eyes", "winner", "winning", "you are a winner", "you have been selected", "bulk email", "buy direct", "cancel at any time", "check or money order", "congratulations", "confidentiality", "cures", "dear friend", "direct email", "direct marketing", "hidden charges", "human growth hormone", "internet marketing", "lose weight", "mass email", "meet singles", "multi-level marketing", "no catch", "no cost", "no credit check", "no fees", "no gimmick", "no hidden costs", "no hidden fees", "no interest", "no investment", "no obligation", "no purchase necessary", "no questions asked", "no strings attached", "not junk", "notspam", "obligation", "passwords", "requires initial investment", "social security number", "this isn’t a scam", "this isn’t junk", "this isn’t spam", "undisclosed", "unsecured credit", "unsecured debt", "unsolicited", "valium", "viagra", "vicodin", "we hate spam", "weight loss", "xanax", "accept credit cards", "ad", "all new", "as seen on", "bargain", "beneficiary", "billing", "bonus", "cards accepted", "cash", "certified", "cheap", "claims", "clearance", "compare rates", "credit card offers", "deal", "debt", "discount", "fantastic", "in accordance with laws", "income", "investment", "join millions", "lifetime", "loans", "luxury", "marketing solution", "message contains", "mortgage rates", "name brand", "offer", "online marketing", "opt in", "pre-approved", "quote", "rates", "refinance", "removal", "reserves the right", "score", "search engine", "sent in compliance", "subject to…", "terms and conditions", "trial", "unlimited", "warranty", "web traffic", "work from home", "$"]

class MyFilter():
    def __init__(self):
        self.corpus = None
        self.train_files = None
        self.spam_files_num = 0
        self.ham_files_num = 0
        self.train_spam_words = defaultdict(int)
        self.train_ham_words = defaultdict(int)
        self.spam_words_num = 0
        self.ham_words_num = 0

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

    def find_files(self):
        pass

    def get_truth_data(self, train_corpus_dir): # open truth file and add a SPAM/HAM tag to each record in train_files
        truth_file = open(os.path.join(train_corpus_dir, '!truth.txt'), 'r', encoding='utf-8')
        for line in truth_file:
            split_line = line.split()
            if split_line[1] == 'SPAM':
                self.train_files[split_line[0]][1] = True
            else:
                self.train_files[split_line[0]][1] = False
        pass
                
    def gather_used_words(self, text, is_spam):
        for line in text:
            for word in line.split():
                word = word.lower()
                word = word.translate(str.maketrans('', '',string.punctuation))
                if len(word) > 3 and is_spam == True:
                    self.train_spam_words[word] += 1
                    self.spam_words_num += 1
                elif len(word) > 3 and is_spam == False:
                    self.train_ham_words[word] += 1
                    self.ham_words_num += 1

    def train(self, train_corpus_dir):
        self.corpus = Corpus(train_corpus_dir)
        self.train_files = self.corpus.emails() # train_files[i][0] -> name of the email file, train_file[i][1] -> contents of the email file
        counter = 0
        self.get_truth_data(train_corpus_dir)
        for file in self.train_files.values():
            (header, contents) = self.split_header_and_contents(file[0]) # split to work with header and contents separately
            counter += 1

            self.gather_used_words(contents, file[1]) # process used words and put them into ham/spam words dictionaries
            if file[1] == True:
                self.spam_files_num += 1
            else:
                self.ham_files_num += 1
                
        return

    def test(self, test_corpus_dir):
        self.corpus = Corpus(test_corpus_dir)
        self.test_files = self.corpus.emails()


x = MyFilter()
x.train('data/1')