import operator
import math

'''
Generate unigrams from given list of words
'''
def generateUnigrams(tokens):
    grams = []
    for idx, item in enumerate(tokens[:]):
        grams.append((item))
    return grams

'''
Generate bigrams for given list of words and distance
for distance = 2: (A, B), (B, C); (B, C), (C, D); (C, D), (D, E); (D, E), (E, F); (E, F)
'''
def generateBigrams(tokens, distance):
    grams = []
    for i, item in enumerate(tokens[:]):
        for j in range(1, distance+1):
            if i+j < len(tokens):
                grams.append((tokens[i+j-1], tokens[i+j]))
            else:
                break
    return grams

'''
Generate bigrams for given list of words and distance
for distance = 2: (A, B), (A, C); (B, C), (B, D); (C, D), (C, E); (D, E), (D, F); (E, F)
'''
def generateBigrams2(tokens, distance):
    grams = []
    for i, item in enumerate(tokens[:]):
        for j in range(1, distance+1):
            if i+j < len(tokens):
                grams.append((item, tokens[i+j]))
            else:
                break
    return grams

'''
Generate bigrams for given list of words and distance
for distance = 2: (A, C); (B, D); (C, E); (D, F); (E, B); (F, B)
'''
def generateBigrams3(tokens, distance):
    grams = []
    for i, item in enumerate(tokens[:]):
        for j in range(1 if distance == 1 else 2, distance+1):
            if i+j >= len(tokens):
                grams.append((item, tokens[-1+j]))
            else:
                grams.append((item, tokens[i+j]))
    return grams

'''
Generate bigrams for given list of words and distance
for distance = 2: (A, C); (B, D); (C, E); (D, F)
'''
def generateBigrams4(tokens, distance):
    grams = []
    for i, item in enumerate(tokens[:]):
        for j in range(1 if distance == 1 else 2, distance+1):
            if i+j < len(tokens):
                grams.append((item, tokens[i+j]))
    return grams

'''
Generate bigrams for given list of words and distance
for distance = 2: (A, C); (B, D); (C, E); (D, F)
'''
def generateBigrams5(tokens, distance):
    grams = []
    for idx, item in enumerate(tokens[:]):
        for i in range(1 if distance == 1 else 2, distance+1):
            if(idx+i) > len(tokens)-1: break
            grams.append((item, tokens[i+idx]))
    return grams

'''
Calculate counts of N-grams (unigrams, bigrams)
'''
def countNgram(ngrams):
    cgrams = {}
    for item in ngrams:
        cgrams[item] = (cgrams[item]+1) if item in cgrams else 1
    return cgrams

'''
Calculate Pointwise Mutual Information for given unigram, bigram and minimal treshold of occurencies of unigrams
'''
def pmi(unigram, bigram, treshold):
    N = 0
    pmi = {}

    for key in bigram.keys():
        N = N + (bigram[key] if (unigram[key[0]] >= treshold and unigram[key[1]] >= treshold) else 0)
    #print('N count %d' % N)

    for key in bigram.keys():
        if (unigram[key[0]] >= treshold and unigram[key[1]] >= treshold):
            pmi[key] = math.log(1.0 * (bigram[key] * N) / (unigram[key[0]] * unigram[key[1]]),2)

    sorted_pmi = sorted(pmi.items(), key=operator.itemgetter(1), reverse = True)
    return sorted_pmi

'''
Calculate Pointwise Mutual Information for given unigram, bigram and minimal treshold of occurencies of unigrams
'''
def pmi2(unigram, bigram, treshold):
    Nbi = sum(bigram.values()) * 1.0
    Nu0 = sum(unigram.values()) * 1.0
    Nu1 = sum(unigram.values()) * 1.0

    pmi = {}
    for key in bigram.keys():
        if (unigram[key[0]] >= treshold and unigram[key[1]] >= treshold):
            pmi[key] = math.log(1.0 * (bigram[key] / Nbi) / ((unigram[key[0]] / Nu0) * (unigram[key[1]] / Nu1)),2)

    sorted_pmi = sorted(pmi.items(), key=operator.itemgetter(1), reverse = True)
    return sorted_pmi
