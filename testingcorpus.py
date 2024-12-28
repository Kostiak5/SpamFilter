import os
import string
import math
from corpus import Corpus 
from collections import defaultdict
IS_SPAM = True
IS_HAM = False
HIGH_OCCURENCE_COEFF = 0.001
SMOOTHING_COEFF = 1 # to avoid situation where spam_coeff would be multiplied to 0 
COMMON_SPAM_WORDS = ["#1", "100% more", "100% free", "100% satisfied", "additional income", "be your own boss", "best price", "big bucks", "billion", "cash bonus", "cents on the dollar", "consolidate debt", "double your cash", "double your income", "earn extra cash", "earn money", "eliminate bad credit", "extra cash", "extra income", "expect to earn", "fast cash", "financial freedom", "free access", "free consultation", "free gift", "free hosting", "free info", "free investment", "free membership", "free money", "free preview", "free quote", "free trial", "full refund", "get out of debt", "get paid", "giveaway", "guaranteed", "increase sales", "increase traffic", "incredible deal", "lower rates", "lowest price", "make money", "million dollars", "miracle", "money back", "once in a lifetime", "one time", "pennies a day", "potential earnings", "prize", "promise", "pure profit", "risk-free", "satisfaction guaranteed", "save big money", "save up to", "special promotion", "act now", "apply now", "become a member", "call now", "click below", "click here", "get it now", "do it today", "don’t delete", "exclusive deal", "get started now", "important information regarding", "information you requested", "instant", "limited time", "new customers only", "order now", "please read", "see for yourself", "sign up free", "take action", "this won’t last", "urgent", "what are you waiting for?", "while supplies last", "will not believe your eyes", "winner", "winning", "you are a winner", "you have been selected", "bulk email", "buy direct", "cancel at any time", "check or money order", "congratulations", "confidentiality", "cures", "dear friend", "direct email", "direct marketing", "hidden charges", "human growth hormone", "internet marketing", "lose weight", "mass email", "meet singles", "multi-level marketing", "no catch", "no cost", "no credit check", "no fees", "no gimmick", "no hidden costs", "no hidden fees", "no interest", "no investment", "no obligation", "no purchase necessary", "no questions asked", "no strings attached", "not junk", "notspam", "obligation", "passwords", "requires initial investment", "social security number", "this isn’t a scam", "this isn’t junk", "this isn’t spam", "undisclosed", "unsecured credit", "unsecured debt", "unsolicited", "valium", "viagra", "vicodin", "we hate spam", "weight loss", "xanax", "accept credit cards", "ad", "all new", "as seen on", "bargain", "beneficiary", "billing", "bonus", "cards accepted", "cash", "certified", "cheap", "claims", "clearance", "compare rates", "credit card offers", "deal", "debt", "discount", "fantastic", "in accordance with laws", "income", "investment", "join millions", "lifetime", "loans", "luxury", "marketing solution", "message contains", "mortgage rates", "name brand", "offer", "online marketing", "opt in", "pre-approved", "quote", "rates", "refinance", "removal", "reserves the right", "score", "search engine", "sent in compliance", "subject to…", "terms and conditions", "trial", "unlimited", "warranty", "web traffic", "work from home"]
# most common spam words/phrases, source: https://www.activecampaign.com/blog/spam-words
COMMON_SUSPICIOUS_SIGNS = ['!', '#', '</', '$', '€'] # anything regarding money, too many excl. signs etc.
HTML_TAGS = ['<html>', '<HTML>', '</html>', '</HTML'] # HTML tags are often used in spam mails

class TestingCorpus(Corpus): 
    def __init__(self, corpus_dir, spam_words, ham_words, spam_words_num, ham_words_num, max_word_length, spam_files_num, ham_files_num):
        self.corpus_dir = corpus_dir
        self.test_files = self.emails()
        self.spam_words = spam_words
        self.ham_words = ham_words
        self.spam_words_num = spam_words_num # number of spam words in the training corpus (each word under max_word_length is counted, incl. duplicities)
        self.ham_words_num = ham_words_num
        self.word_spam_score = 0 # will be set for each word when test_mail function is called
        self.word_ham_score = 0
        self.max_word_length = max_word_length # set constant which determines how long a string could be to still be counted as a word
        self.spam_files_num = spam_files_num
        self.ham_files_num = ham_files_num

    def all_spam_words_coeff(self): # ratio of spam words to all words in our training set
        return ((self.spam_files_num) / (self.ham_files_num + self.spam_files_num))
    
    def all_ham_words_coeff(self): # ratio of ham words to all words in our training set
        return (self.ham_files_num / (self.ham_files_num + self.spam_files_num))
    
    def this_spam_word_coeff(self, this_word_occurence): 
        return ((this_word_occurence * 1000 + SMOOTHING_COEFF) / (self.spam_words_num + SMOOTHING_COEFF * 2))
        # this_word_occurence = how many times this word was used in training set spam mails
        # smoothing_coeff = constant, can be edited manually (value 1.0 proved to be the most effective)
        # spam_words_num = number of all spam words in training set
        # ham_words_num = number of all ham words in training set
    
    def this_ham_word_coeff(self, this_word_occurence):
        return ((this_word_occurence * 1000 + SMOOTHING_COEFF) / (self.ham_words_num + SMOOTHING_COEFF * 2))
        # this_word_occurence = how many times this word was used in training set ham mails
        # smoothing_coeff = constant, can be edited manually (value 1.0 proved to be the most effective)
        # spam_words_num = number of all spam words in training set
        # ham_words_num = number of all ham words in training set

    def check_uppercase(self, word, score):
        if word.isupper() == True:
            return (score + 1)

        return score
    
    def check_suspicious_signs_word(self, word, score):
        for sign in COMMON_SUSPICIOUS_SIGNS:
            if word.count(sign) >= 2:
                score += 1
        
        return score

    def check_suspicious_signs_text(self, text, score):
        for sign in COMMON_SUSPICIOUS_SIGNS:
            if text.count(sign) >= 5:
                score += 20
            if text.count(sign) >= 2:
                score += 3

        
        for tag in HTML_TAGS:
            if text.count(tag) >= 1:
                score += 30
        
        return score
    
    def check_standard_spam_words(self, word, score):
        if word in COMMON_SPAM_WORDS:
            score += 5

        return score
    
    def analyze_used_words(self, text):
        spam_coeff = self.all_spam_words_coeff()
        ham_coeff = self.all_ham_words_coeff()

        for word in text:
            if len(word) > self.max_word_length:
                continue
            
            #print(spam_coeff)
            #print(ham_coeff)
            prev_spam_coeff = spam_coeff
            if word in self.spam_words:
                #print('S', word, self.spam_words[word], spam_coeff, self.this_spam_word_coeff(self.spam_words[word]))
                spam_coeff *= self.this_spam_word_coeff(self.spam_words[word])
            else:
                spam_coeff *= self.this_spam_word_coeff(0)

            prev_ham_coeff = ham_coeff
            if word in self.ham_words:
                #print('H', word, self.ham_words[word], ham_coeff, self.this_ham_word_coeff(self.ham_words[word]))   
                ham_coeff *= self.this_ham_word_coeff(self.ham_words[word])
            else:
                ham_coeff *= self.this_ham_word_coeff(0)
            
            if (spam_coeff == math.inf and ham_coeff == math.inf) or (spam_coeff == 0.0 and ham_coeff == 0.0):
                spam_coeff = prev_spam_coeff
                ham_coeff = prev_ham_coeff
                break
            elif spam_coeff == math.inf or ham_coeff == 0.0:
                spam_coeff = prev_spam_coeff
                break
            elif ham_coeff == math.inf or ham_coeff == 0.0:
                ham_coeff = prev_ham_coeff
                break
        
        if abs(spam_coeff - ham_coeff) > 0:
            if spam_coeff > ham_coeff:
                return IS_SPAM
            else:
                return IS_HAM
        else:
            print('ndecided', spam_coeff, ham_coeff)
            return IS_HAM
    
    def add_to_spam_score(self, score):
        if score >= 15: # if there are enough points in this score category, it raises the suspicion that this email is a spam
            self.spam_score += score

    def analyze_contents_format(self, text):
        # define 3 score categories: score for uppercase words, identified standard spam words and suspicious signs
        uppercase_score = 0
        standard_spam_words_score = 0
        suspicious_signs_score = 0

        for word in text:
            if len(word) > self.max_word_length:
                continue
            standard_spam_words_score = self.check_standard_spam_words(word, standard_spam_words_score)
            uppercase_score = self.check_uppercase(word, uppercase_score) # increase score in case there are full uppercase words
            suspicious_signs_score = self.check_suspicious_signs_word(word, suspicious_signs_score)
        
        suspicious_signs_score += self.check_suspicious_signs_text(text, suspicious_signs_score)

        # evaluate whether score is enough to label it as a spam sign
        self.add_to_spam_score(standard_spam_words_score)
        self.add_to_spam_score(uppercase_score)
        self.add_to_spam_score(suspicious_signs_score)
    
    def test_mail(self, file_name):
        self.spam_score = 0
        self.ham_score = 0
        (header, contents) = self.split_header_and_contents(self.test_files[file_name][0])
        used_words_indicator = False
        if self.spam_words_num != 0 and self.ham_words_num != 0:
            used_words_indicator = self.analyze_used_words(contents)
            if used_words_indicator == IS_SPAM:
                return IS_SPAM
            elif used_words_indicator == IS_HAM:
                return IS_HAM
            # else: continue (the difference is too small)
        
        self.analyze_contents_format(contents)
        print(file_name)
        if self.spam_score >= 50:
            return IS_SPAM
        else:
            return IS_HAM
       
        


        
