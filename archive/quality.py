import os
from confmat import BinaryConfusionMatrix
from utils import read_classification_from_file

def quality_score(tp, tn, fp, fn):
    q = (tp + tn) / (tp + tn + 10*fp + fn)
    return q

def compute_quality_for_corpus(corpus_dir):
    tr_path = os.path.join(corpus_dir, '!truth.txt')
    pr_path = os.path.join(corpus_dir, '!prediction.txt')

    tr_dict = read_classification_from_file(tr_path)
    pr_dict = read_classification_from_file(pr_path)
    cm = BinaryConfusionMatrix(pos_tag='SPAM', neg_tag='OK')
    cm.compute_from_dicts(tr_dict, pr_dict)

    cm_dict = cm.as_dict()

    score = quality_score(cm_dict['tp'], cm_dict['tn'], cm_dict['fp'], cm_dict['fn'])
    return score

