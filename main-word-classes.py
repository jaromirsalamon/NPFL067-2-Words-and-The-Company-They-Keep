# coding: utf-8

from bf import *
from wc import *
import codecs
import os

def calculate(fileIn, fileOut, limit, variant, enc):
    # data structures
    mi = 0              # mutual information
    uniqueTermsLen = 0  # unique(i)
    cUnigram = {}       # ck(i)   unigram counts
    cBigram = {}        # ck(i,j) bigram counts
    cUnigramL = {}      # ckl(i)  unigram counts left
    cUnigramR = {}      # ckr(j)  unigram counts right
    q = {}              # qk(i,j) subterms
    s = {}              # sk(a)   substractions
    l = {}              # Lk(a,b) table of losses
    classes = {}        # classes
    occurringLimit = 10 # for words 10 occurencies limit, for tags 5

    lines_temp = []
    lines = []
    fileName, fileExt = os.path.splitext(fileOut)

    print "read data from file: " +  fileIn
    for line in codecs.open(fileIn, "r", encoding=enc).readlines():
        if variant == "words":
            lines_temp.append(line.strip().split("/")[0])
        else:
            lines_temp.append(line.strip().split("/")[1])
    lines = lines_temp[0:limit]
    print "total lines: " + str(len(lines)) + " / " + str(len(lines_temp)) +  " based on limit: " + str(limit)

    if variant == "words":
        occurringLimit = 10
    else:
        occurringLimit = 5

    N = len(lines) * 1.0

    print 'count of all unigrams...'
    cUnigram = countNgram(generateUnigrams(lines))

    print('count of all bigrams...')
    cBigram = countNgram(generateBigrams(lines,1))

    cUnigramL = {}
    cUnigramR = {}
    for key in cBigram.keys():
            cUnigramL[key[0]] = cUnigram[key[0]]
            cUnigramR[key[1]] = cUnigram[key[1]]

    print('count of frequent words and create initial classes...')
    for item, count in cUnigramR.items():
        if count >= occurringLimit:
            classes[item] = item

    print 'unique frequent word count...'
    uniqueTerms = list(set(classes.keys()))

    print 'writing file: ' + fileName + '-' + variant + fileExt
    file = codecs.open(fileName + '-' + variant + fileExt, "w", encoding = "utf-8")

    while True:
        print 'calculate subterms MI and total MI...'
        mi, q = calcQ(cUnigram, cBigram, N, q)

        print 'calculate substractions...'
        s = calcS(uniqueTerms, cUnigramL, cUnigramR, q)

        print 'calculate table of loses...'
        minl, wordA, wordB = calcL(uniqueTerms, cUnigramL, cUnigramR, cBigram, N, q, s)

        print 'mergee classes...'
        uniqueTerms, cBigram, cUnigramL, cUnigramR, classes = doClassesMerge(uniqueTerms, cBigram, cUnigramL, cUnigramR, classes, wordA, wordB)

        print 'for ' + str(len(classes)) + ' classes is mutual information: ' + str(mi) + ' minimal loss: ' + str(minl) + ' for ' + t(wordA, classes)
        file.write('for ' + str(len(classes)) + ' classes is mutual information: ' + str(mi) + ' minimal loss: ' + str(minl) + ' for ' + t(wordA, classes) + '\n')
        N -= 1
        if len(classes) == 1: break
        if len(classes) == 15: classes15 = classes.copy()

    file.close()

    print 'writing file: ' + fileName + '-' + variant + '-15' + fileExt
    file = codecs.open(fileName + '-' + variant + '-15' + fileExt, "w", encoding="utf-8")

    i = len(classes15)
    for key, val in classes15.items():
        print 'class #' + str(i) + ' is key: ' + key + ' -> ' + val
        file.write('class #' + str(i) + ' is: ' + val + '\n')
        i -= 1

    file.close()

fileIn  = 'input/TEXTEN1.ptg'
fileOut = 'output/merged-classes-EN.txt'
calculate(fileIn, fileOut,8000,'words','ascii')
calculate(fileIn, fileOut,-1,'tags','ascii')

fileIn  = 'input/TEXTCZ1.ptg'
fileOut = 'output/merged-classes-CZ.txt'
calculate(fileIn, fileOut,8000,'words','iso8859_2')
calculate(fileIn, fileOut,800,'tags','iso8859_2')