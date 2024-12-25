import os

class Corpus():
    def __init__(self, corpus_dir):
        self.corpus_dir = corpus_dir
        
    def emails(self): # train_files[i][0] -> name of the email file, train_file[i][1] -> contents of the email file
        email_dict = {}
        for file in os.listdir(self.corpus_dir):
            if file[0] != '!':
                
                file_path = os.path.join(self.corpus_dir, file)
                open_file = open(file_path, "r", encoding='utf-8')
                file_content = open_file.read()
                email_dict[file] = [file_content, ''] # 1st element -> header and contents of the email, 2nd element -> spam/ham
                open_file.close()
        
        return email_dict

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

