from scipy.special import comb
import numpy as np

def get_true_positives(matrix):

    TP = 0
    for i in range(matrix.shape[1]):
        for j in range(matrix.shape[0]):
            TP = TP + comb(matrix[j][i], 2, exact=True)
            
    return TP

def get_false_positives(matrix):

    TP_FP = 0
    sum_array = np.sum(matrix, axis=0)
    for i in range(sum_array.shape[0]):
        TP_FP = TP_FP + comb(sum_array[i], 2, exact=True)
        
    TP = 0
    for i in range(matrix.shape[1]):
        for j in range(matrix.shape[0]):
            TP = TP + comb(matrix[j][i], 2, exact=True)
        
    return TP_FP - TP

def get_false_negatives(matrix):    
    FN = 0

    labels = matrix.shape[0]

    clusters = matrix.shape[1]

    for label in range(labels):
        for cluster_ in range(clusters):
            for cluster in range(cluster_ + 1,clusters):

                FN = FN + matrix[label][cluster_] * matrix[label][cluster]
                
    return FN

def get_precision(matrix):

	tp = get_true_positives(matrix)
	fp = get_false_positives(matrix)

	return tp / (tp + fp)

def get_recall(matrix):

	tp = get_true_positives(matrix)
	fn = get_false_negatives(matrix)

	return tp / (tp + fn)

def get_f_measure(matrix):

	precision = get_precision(matrix)
	recall = get_recall(matrix)

	return 2 * precision * recall / (precision + recall)