import os
from corpus import Corpus 

class TrainingCorpus(Corpus):    
    def get_class(self, file_name): 
        # vstupem bude název souboru s emailem a výstupem buď kód OK nebo SPAM
        truth_file_path = os.path.join(self.path, "1/!truth.txt")
        truth_file = open(truth_file_path, 'r')
        file_names = truth_file.read().split() 
        print(file_names)
        if file_name not in file_names:
            print("FILE NOT FOUND")
            return None
        else:
            return file_names[file_names.index(file_name) + 1]

