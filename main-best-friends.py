# coding: utf-8

from bf import *
import math
import codecs

def calculate (fileIn, fileOut, distance, enc):
    print "read data from file: " + fileIn
    lines = []
    for line in codecs.open(fileIn, "r", encoding=enc).readlines():
        lines.append(line.strip())

    limit = 20 #limit of output to file
    print "len lines: " + str(len(lines))

    print "count unigrams..."
    cUnigram = countNgram(generateUnigrams(lines))
    print("len unigram: " + str(len(cUnigram)))
    #for key in cUnigram.keys():
    #    print "key: \t" + key + ", value:\t" + str(cUnigram[key])
    
    print "count bigrams..."
    cBigram = countNgram(generateBigrams5(lines,distance))
    #for key in cBigram.keys():
    #    print "key: \t" + str(key) + ", value:\t" + str(cBigram[key])

    print "len bigram: " + str(len(cBigram))
    print "sum bigram: " + str(sum(cBigram.values()))

    print "calculate PMI..."
    pmi = pmi2(cUnigram, cBigram, 10.0) #10 is limit of occurrences

    count = 0
    print "store data in file: " + fileOut
    file = codecs.open(fileOut, "w", encoding ="utf-8")
    
    for item in pmi:
        count += 1
        if count > limit: break
        print ", ".join(item[0]) + "\t" + "{:.9f}".format(item[1])
        file.write(", ".join(item[0]) + "\t" + "{:.9f}".format(item[1])  + '\n')

    file.close()

'''
fileIn  = 'input/test.txt'
fileOut = 'output/best-friends-test.txt'
calculate(fileIn, fileOut,2,"iso8859_2")
'''

fileIn  = 'input/TEXTCZ1.txt'
fileOut = 'output/best-friends-CZ-close.txt'
calculate(fileIn, fileOut, 1, "iso8859_2")

fileOut = 'output/best-friends-CZ-far.txt'
calculate(fileIn, fileOut, 50, "iso8859_2")


fileIn  = 'input/TEXTEN1.txt'
fileOut = 'output/best-friends-EN-close.txt'
calculate(fileIn, fileOut, 1, "ascii")

fileOut = 'output/best-friends-EN-far.txt'
calculate(fileIn, fileOut, 50, "ascii")