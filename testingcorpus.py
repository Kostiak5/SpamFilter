import os
import string
from corpus import Corpus 
from collections import defaultdict
IS_SPAM = True
IS_HAM = False
HIGH_OCCURENCE_COEFF = 0.001
SMOOTHING_COEFF = 1.0
COMMON_SPAM_WORDS = ["#1", "100% more", "100% free", "100% satisfied", "additional income", "be your own boss", "best price", "big bucks", "billion", "cash bonus", "cents on the dollar", "consolidate debt", "double your cash", "double your income", "earn extra cash", "earn money", "eliminate bad credit", "extra cash", "extra income", "expect to earn", "fast cash", "financial freedom", "free access", "free consultation", "free gift", "free hosting", "free info", "free investment", "free membership", "free money", "free preview", "free quote", "free trial", "full refund", "get out of debt", "get paid", "giveaway", "guaranteed", "increase sales", "increase traffic", "incredible deal", "lower rates", "lowest price", "make money", "million dollars", "miracle", "money back", "once in a lifetime", "one time", "pennies a day", "potential earnings", "prize", "promise", "pure profit", "risk-free", "satisfaction guaranteed", "save big money", "save up to", "special promotion", "act now", "apply now", "become a member", "call now", "click below", "click here", "get it now", "do it today", "don’t delete", "exclusive deal", "get started now", "important information regarding", "information you requested", "instant", "limited time", "new customers only", "order now", "please read", "see for yourself", "sign up free", "take action", "this won’t last", "urgent", "what are you waiting for?", "while supplies last", "will not believe your eyes", "winner", "winning", "you are a winner", "you have been selected", "bulk email", "buy direct", "cancel at any time", "check or money order", "congratulations", "confidentiality", "cures", "dear friend", "direct email", "direct marketing", "hidden charges", "human growth hormone", "internet marketing", "lose weight", "mass email", "meet singles", "multi-level marketing", "no catch", "no cost", "no credit check", "no fees", "no gimmick", "no hidden costs", "no hidden fees", "no interest", "no investment", "no obligation", "no purchase necessary", "no questions asked", "no strings attached", "not junk", "notspam", "obligation", "passwords", "requires initial investment", "social security number", "this isn’t a scam", "this isn’t junk", "this isn’t spam", "undisclosed", "unsecured credit", "unsecured debt", "unsolicited", "valium", "viagra", "vicodin", "we hate spam", "weight loss", "xanax", "accept credit cards", "ad", "all new", "as seen on", "bargain", "beneficiary", "billing", "bonus", "cards accepted", "cash", "certified", "cheap", "claims", "clearance", "compare rates", "credit card offers", "deal", "debt", "discount", "fantastic", "in accordance with laws", "income", "investment", "join millions", "lifetime", "loans", "luxury", "marketing solution", "message contains", "mortgage rates", "name brand", "offer", "online marketing", "opt in", "pre-approved", "quote", "rates", "refinance", "removal", "reserves the right", "score", "search engine", "sent in compliance", "subject to…", "terms and conditions", "trial", "unlimited", "warranty", "web traffic", "work from home"]
# most common spam words/phrases, source: https://www.activecampaign.com/blog/spam-words
COMMON_SUSPICIOUS_SIGNS = ['!', '#', '<', '>', '$', '€'] # anything regarding money, too many excl. signs, HTML tags

class TestingCorpus(Corpus): 
    def __init__(self, corpus_dir, spam_words, ham_words, spam_words_num, ham_words_num, max_word_length):
        self.corpus_dir = corpus_dir
        self.test_files = self.emails()
        self.spam_words = spam_words
        self.ham_words = ham_words
        self.spam_words_num = spam_words_num # number of spam words in the training corpus (each word under max_word_length is counted, incl. duplicities)
        self.ham_words_num = ham_words_num
        self.word_spam_score = 0 # will be set for each word when test_mail function is called
        self.word_ham_score = 0
        self.max_word_length = max_word_length # set constant which determines how long a string could be to still be counted as a word
    
    def all_spam_words_coeff(self): # ratio of spam words to all words in our training set
        return self.spam_words_num / (self.ham_words_num + self.spam_words_num)
    
    def all_ham_words_coeff(self): # ratio of ham words to all words in our training set
        return self.ham_words_num / (self.ham_words_num + self.spam_words_num)
    
    def this_spam_word_coeff(self, this_word_occurence): 
        return (this_word_occurence + SMOOTHING_COEFF) / (self.spam_words_num + SMOOTHING_COEFF * (self.spam_words_num + self.ham_words_num))
        # this_word_occurence = how many times this word was used in training set spam mails
        # smoothing_coeff = constant, can be edited manually (value 1.0 proved to be the most effective)
        # spam_words_num = number of all spam words in training set
        # ham_words_num = number of all ham words in training set
    
    def this_ham_word_coeff(self, this_word_occurence):
        return (this_word_occurence + SMOOTHING_COEFF) / (self.ham_words_num + SMOOTHING_COEFF * (self.spam_words_num + self.ham_words_num))
        # this_word_occurence = how many times this word was used in training set ham mails
        # smoothing_coeff = constant, can be edited manually (value 1.0 proved to be the most effective)
        # spam_words_num = number of all spam words in training set
        # ham_words_num = number of all ham words in training set
    
    def is_of_high_occurence(self, word_occurence):
        if word_occurence / (self.spam_words_num + self.ham_words_num) > HIGH_OCCURENCE_COEFF:
            return True
        else:
            return False
        
    def analyze_word_occurence(self, occurence, score):
        if self.is_of_high_occurence(occurence):
            return 4
        else:
            return 1

    
    def check_dict_words(self, word, spam_score, ham_score):
        word = self.normalize_word(word) 
        if word in self.spam_words:
            self.spam_score += self.analyze_word_occurence(self.spam_words[word])
        elif word in self.ham_words:
            self.ham_score += self.analyze_word_occurence(self.ham_words[word])
                
        return (spam_score, ham_score)

    def check_uppercase(self, word):
        if word.isupper() == True:
            self.spam_score += 3
    
    def check_suspicious_signs_word(self, word):
        for sign in COMMON_SUSPICIOUS_SIGNS:
            if word.count(sign) >= 2:
                self.spam_score += 1

    def check_suspicious_signs_text(self, text):
        for sign in COMMON_SUSPICIOUS_SIGNS:
            if text.count(sign) >= 5:
                self.spam_score += 8
    
    def check_standard_spam_words(self, word):
        if word in COMMON_SPAM_WORDS:
            self.spam_score += 8
    
    def analyze_used_words(self, text):
        '''
        message: a string
        '''
        spam_coeff = self.spam_words_coeff()
        ham_coeff = self.ham_words_coeff()

        for line in text:
            for word in line.split():
                if len(word) > self.max_word_length:
                    continue

                if word in self.spam_words:
                    spam_coeff *= self.this_spam_word_coeff(self.spam_words[word])

                if word in self.ham_words:
                    ham_coeff *= self.this_ham_word_coeff(self.ham_words[word])

        print('P(Spam|message):', spam_coeff)
        print('P(Ham|message):', ham_coeff)

        if ham_coeff > spam_coeff:
            print('Label: Ham')
        elif ham_coeff < spam_coeff:
            print('Label: Spam')
        else:
            print('Equal proabilities, have a human classify this!')

    def analyze_contents_format(self, text):
        for line in text:
            for word in line.split():
                if len(word) > self.max_word_length:
                    continue
                self.check_standard_spam_words(word)
                self.check_uppercase(word) # increase spam score in case there are full uppercase words
                self.check_suspicious_signs_word(word)
        
        self.check_suspicious_signs_text(text)

    
    def test_mail(self, file_name):
        self.spam_score = 0
        self.ham_score = 0
        (header, contents) = self.split_header_and_contents(self.test_files[file_name][0])
        self.analyze_contents_format(contents)
        self.analyze_used_words(contents)

       



        
