# -*- encoding: utf-8 -*-
__author__ = 'Jaehyun Ahn'
__email__ = 'jaehyunahn@sogang.ac.kr'
"""
    Library List
    - KoNLPy: http://konlpy-ko.readthedocs.org/ko/v0.4.3/
        - JHannanum is a morphological analyzer and POS tagger written in Java, and developed by the Semantic Web Research Center (SWRC) at KAIST since 1999.
    - Word2Vec : https://github.com/danielfrg/word2vec
    - NLTK: http://nltk.org/
"""
from konlpy.tag import Hannanum
from datetime import datetime
from nltk import collocations
import csv

def readTXTfile(name, analyzeType, wordDict):
    """
    :param name: textFile name
    :param analyzeType: NOUNS(명사), MORPHS(형태소분석), n-grams(바이, 트라이)
    :return: dict csv file?
    """
    # read txt file
    file = open(name, 'r')
    lines = file.readlines()
    # load module
    for line in lines:
        # init word list
        wlist = list()
        if(line != '\n') and (line != " \n"):
            # analyze nouns adjective
            if (analyzeType == "nouns"):
                wlist = lineAnalyzer(sentence=line, analyzeType=1)
            elif (analyzeType == "morphs"):
                wlist = lineAnalyzer(sentence=line, analyzeType=2)
            elif (analyzeType == "bigram"):
                wlist = lineAnalyzer(sentence=line, analyzeType=3)
            elif (analyzeType == "trigram"):
                wlist = lineAnalyzer(sentence=line, analyzeType=4)
            else:
                print("[ERROR] There is no type like %s in readTXTfile function." % analyzeType)
                break
        # print(line) # 왜 에러가?
        print(wlist) # 심심하니까..
        wordDict = addDict(listType=wlist,dictionaryType=wordDict)
    file.close()
    return 0

def lineAnalyzer(sentence, analyzeType):
    hannanum = Hannanum()
    wordList = list()
    if (analyzeType == 1):
        # Nouns
        wordList = hannanum.nouns(str(sentence))
    elif (analyzeType == 2):
        # Morphs
        wordList = hannanum.morphs(str(sentence))
    elif (analyzeType == 3):
        # Bi-grams
        bigram_measures = collocations.BigramAssocMeasures()
        pos = hannanum.pos(str(sentence))
        words = [s for s, t in pos]
        finder = collocations.BigramCollocationFinder.from_words(words)
        finder.apply_word_filter(lambda w: len(w) < 2)
        finder.apply_freq_filter(3)
        wordList = finder.nbest(bigram_measures.pmi, 10)
    elif (analyzeType == 4):
        # Tri-grams
        trigram_measures = collocations.TrigramAssocMeasures()
        pos = hannanum.pos(str(sentence))
        words = [s for s, t in pos]
        finder = collocations.TrigramCollocationFinder.from_words(words)
        finder.apply_word_filter(lambda w: len(w) < 2)
        finder.apply_freq_filter(3)
        wordList = finder.nbest(trigram_measures.pmi, 10)
    else:
        print("error on top!")
    return wordList

def addDict(listType, dictionaryType):
    for list in listType:
        if dictionaryType.get(str(list)) is None:
            # add Dictonary
            dictionaryType.update({str(list): 1})
        else:
            # update Dictonary
            count = dictionaryType.get(str(list))
            count = count + 1
            dictionaryType[str(list)] = count
    return dictionaryType

def saveCSVfile(dictonaryType, filename):
    print('CSV writing is started...')
    with open(filename, 'w') as f:
        w = csv.DictWriter(f, dictonaryType.keys())
        for key, val in dictonaryType.items():
            w.writerow([key, val])
        f.close()
    print('Writing CSV is done.')
    return 0

if __name__ == "__main__":
    # project init
    textName = '사랑'
    analyzeType = 'nouns'
    wordDict = dict()

    date = datetime.now()
    print("Project started in ", str(date))
    readTXTfile(name=(textName + ".txt"), analyzeType=analyzeType, wordDict=wordDict)
    saveCSVfile(dictonaryType=wordDict, filename=(textName + analyzeType + '.csv'))
    date = datetime.now()
    print("Project ended in ", str(date))