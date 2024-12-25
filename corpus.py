import os

class Corpus():
    def __init__(self, path):
        self.path = path
        
    def emails(self):
        email_dict = {}
        for file in os.listdir(self.path):
            if file[0] != '!':
                
                file_path = os.path.join(self.path, file)
                open_file = open(file_path, "r", encoding='utf-8')
                file_content = open_file.read()
                email_dict[file] = [file_content, ''] # 1st element -> header and contents of the email, 2nd element -> spam/ham
                open_file.close()
        
        return email_dict

