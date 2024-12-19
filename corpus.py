import os

class Corpus():
    def __init__(self, path):
        self.path = path
        
    def emails(self):
        for file in os.listdir(self.path):
            if file[0] != '!':
                
                file_path = os.path.join(self.path, file)
                open_file = open(file_path, "r", encoding='utf-8')
                file_content = open_file.read()
                yield(file_content)
                open_file.close()
        
        #return []

