import os
import string
import email

class Corpus():
    def __init__(self, corpus_dir):
        self.corpus_dir = corpus_dir
        
    def emails(self):
        email_dict = {}
        for file in os.listdir(self.corpus_dir):
            if file[0] != '!':
                
                file_path = os.path.join(self.corpus_dir, file)
                open_file = open(file_path, "r", encoding='utf-8')
                file_content = open_file.read()
                email_dict[file] = [file_content, ''] # key -> name of file with the email, 1st element -> header and contents of the email, 2nd element -> spam/ham tag
                open_file.close()
        
        return email_dict
    
    def normalize_word(self, word): # lower case and remove punctuation
        word = word.lower()
        word = word.translate(str.maketrans('', '',string.punctuation))
        return word

    def split_header_and_contents(self, file): # split header of an email and contents of it into two separate lists
        header = []
        contents = []
        header_ended = False
        file_lines = file.split('\n')
        for line in file_lines:
            if header_ended == False and line == '':
                header_ended = True
            elif header_ended == True and line != '':
                contents.extend(line.split()) # contents -> list of words
            elif line != '':
                header.append(line) # contents -> list of non-empty lines
        #print(contents)      
        
        return (header, contents)

