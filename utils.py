def read_classification_from_file(fn):
    f = open(fn, "r", encoding='utf-8')
    spam_dict = {}
    for line in f.readlines():
        split_line = line.split()
        spam_dict[split_line[0]] = split_line[1]
    f.close()
    
    return spam_dict
