import operator
import math

'''
Subterms and total mutual information calculation
qk(l,r) = ck(l,r)/N log(N ck(l,r)/(ckl(l) ckr(r)))
'''
def calcQ(cUnigram, cBigram, N, q):
    mi = 0
    for key in cBigram.keys():
        q[key] = cmi(N, cUnigram[key[0]], cUnigram[key[1]], cBigram[key])
        mi += q[key]
    return mi, q

'''
Substractions calculation
sk(a) = sum(l=1..k,qk(l,a)) + sum(r=1..k,qk(a,r)) - qk(a,a)
'''
def calcS(uniqueTerms, cUnigramL, cUnigramR, q):
    s = {}
    for word in uniqueTerms:
        # Note: q[word,word] doesn't exist in this implementation! Anyway it is unigram with MI which is log2(1) = 0
        s[word] = 0
        s[word] = sum(t((wordL, word), q) for wordL in cUnigramL.keys()) + \
                  sum(t((word, wordR), q) for wordR in cUnigramR.keys())
    return s

'''
Calculation of minimal loss L
Lk(a,b) = sk(a)+sk(b)-qk(a,b)-qk(b,a)-qk(a+b,a+b) - sum(l=1..k,l<>a,bqk(l,a+b)) - sum(r=1..k,r<>a,bqk(a+b,r))
'''
def calcL(uniqueTerms, cUnigramL, cUnigramR, cBigram, N, q, s):
    minl = 1000.0
    l = {}

    for a in range(0, len(uniqueTerms)):
        wordA = uniqueTerms[a]
        for b in range(a + 1, len(uniqueTerms)):
            wordB = uniqueTerms[b]

            sumL = 0
            sumR = 0

            cUnigramRAB = cUnigramR[wordA] + cUnigramR[wordB]

            for wordL in cUnigramL.keys():
                if not (wordL == wordA or wordL == wordB):
                    cBigramLAB = t((wordL, wordA), cBigram) + t((wordL, wordB), cBigram)
                    sumL = sumL + cmi(N, cUnigramL[wordL], cUnigramRAB, cBigramLAB)

            # if((wordA == "cannot" and wordB == "may") or (wordA == "may" and wordB == "cannot")):
            #    print("L",wordA, wordB, N, biLwA, biLwB, uniL, cUnigramRAB, sumL)

            cUnigramLAB = cUnigramL[wordA] + cUnigramL[wordB]

            for wordR in cUnigramR.keys():
                if not (wordR == wordA or wordR == wordB):
                    cBigramRAB = t((wordA, wordR), cBigram) + t((wordB, wordR), cBigram)
                    sumR = sumR + cmi(N, cUnigramR[wordR], cUnigramLAB, cBigramRAB)

            # if((wordA == "cannot" and wordB == "may") or (wordA == "may" and wordB == "cannot")):
            #    print("R",wordA, wordB, N, biRwA, biRwB, uniR, cUnigramLAB, sumR)

            cBigramAB = t((wordA, wordA), cBigram) + t((wordA, wordB), cBigram) + t((wordB, wordA), cBigram) + t((wordB, wordB), cBigram)
            l[(wordA, wordB)] = s[wordA] + s[wordB] - t((wordA, wordB), q) - t((wordB, wordA), q) - \
                                cmi(N,cUnigramLAB,cUnigramRAB,cBigramAB) - sumL - sumR

            # if ((wordA == "case" and wordB == "subject") or (wordA == "subject" and wordB == "case")):
            #    print 'Minimal loss: ' + str(l[(wordA, wordB)]) + ' for ' + wordA + '+' + wordB

            if (l[(wordA, wordB)] < minl):
                minl = l[(wordA, wordB)]
                minWordA = wordA
                minWordB = wordB

    return minl, minWordA, minWordB

'''
Merge classes
'''
def doClassesMerge(uniqueTerms, cBigram, cUnigramL, cUnigramR, classes, wordA, wordB):
    # merge counts of unigram wordA and unigram wordB into unigram wordA and delete unigram wordB
    cUnigramL[wordA] = cUnigramL[wordA] + cUnigramL[wordB]
    del cUnigramL[wordB]
    cUnigramR[wordA] = cUnigramR[wordA] + cUnigramR[wordB]
    del cUnigramR[wordB]

    # merge classes
    classes[wordA] = classes[wordA] + "+" + classes[wordB]
    del classes[wordB]

    # update uniqueTerms
    uniqueTerms.remove(wordB)

    # merge counts of bigram
    cBigramAux = cBigram.copy()
    for key in cBigram.keys():
        if key[0] == wordB:
            if key[1] == wordB:
                '''key[0],key[1] = minWordB,minWordB'''
                if (t((wordB, wordB), cBigramAux) > 0) and (t((wordA, wordA), cBigramAux) > 0):
                    cBigramAux[(wordA, wordA)] += cBigramAux[(wordB, wordB)]
                    del cBigramAux[(wordB, wordB)]
                else:
                    cBigramAux[(wordA, wordA)] = 0
            else:
                '''key[0],key[1] = minWordB,key[1]'''
                if (t((wordB, key[1]), cBigramAux) > 0) and (t((wordA, key[1]), cBigramAux) > 0):
                    cBigramAux[(wordA, key[1])] += cBigramAux[(wordB, key[1])]
                    del cBigramAux[(wordB, key[1])]
                else:
                    cBigramAux[(wordA, key[1])] = 0
        else:
            if key[1] == wordB:
                '''key[0],key[1] = key[0],minWordB'''
                if (t((key[0], wordB), cBigramAux) > 0) and (t((wordA, wordB), cBigramAux) > 0):
                    cBigramAux[(wordA, wordB)] += cBigramAux[(key[0], wordB)]
                    del cBigramAux[(key[0], wordB)]
                else:
                    cBigramAux[(wordA, wordB)] = 0
                # else:
                '''key[0],key[1] = key[0],key[1] - not necessary to care :-)'''

    return uniqueTerms, cBigramAux, cUnigramL, cUnigramR, classes

'''
Calculate Mutual Information
'''
def cmi(N, cx, cy, cxy):
    return ((cxy / N) * math.log(1.0 * (cxy * N) / (cx * cy), 2)) if (1.0 * (cxy * N) / (cx * cy) > 0) else 0

'''
Test if key i exists in dictionary d and return it's value or 0
'''
def t(key, dictionary):
    # key is item in dictionary d or not :-)
    return dictionary[key] if key in dictionary else 0
