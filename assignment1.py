import re
import random
import math
import sys

"""

Emre COSKUNCAY
BBM 497 - NLP LAB. ASSIGNMENT 1 
21526806

Thanks to this assignment, I made an introduction and practice to natural language processing. 
I'm interested in this subject. I hope I will be more successful in NLP. Thank you.

"""

#The file path where the data folder is located should be given.
path = "./data/"
hamiltonTexts=["1.txt","6.txt","7.txt","8.txt","13.txt","15.txt","16.txt","17.txt","21.txt","22.txt","23.txt","24.txt","25.txt","26.txt","27.txt","28.txt","29.txt"]
hamilton_Test=["9.txt","11.txt","12.txt"]
madisonTexts=["10.txt","14.txt","37.txt","38.txt","39.txt","40.txt","41.txt","42.txt","43.txt","44.txt","45.txt","46.txt"]
madison_Test=["47.txt","48.txt","58.txt"]
unknownTexts = ["49.txt","50.txt","51.txt","52.txt","53.txt","54.txt","55.txt","56.txt","57.txt","62.txt","63.txt"]

# since I haven't coded in python for a long time. The next assignment will be better.
hamiltonUnknown=[]
madisonUnknown=[]
totalUnknown=[]
madisonUniGeneral=[]
madisonUniFrequency={}
madisonUniPossibility={}
madisonBiGeneral=[]
madisonBiFrequency={}
madisonBiPossibility={}
madisonTriGeneral=[]
madisonTriFrequency={}
madisonTriPossibility={}

hamiltonUniGeneral=[]
hamiltonUniFrequency={}
hamiltonUniPossibility={}
hamiltonBiGeneral=[]
hamiltonBiFrequency={}
hamiltonBiPossibility={}
hamiltonTriGeneral=[]
hamiltonTriFrequency={}
hamiltonTriPossibility={}

totalFrequency= [madisonUniFrequency,madisonBiFrequency,madisonTriFrequency,hamiltonUniFrequency,hamiltonBiFrequency,hamiltonTriFrequency]
totalGeneral= [madisonUniGeneral,madisonBiGeneral,madisonTriGeneral,hamiltonUniGeneral,hamiltonBiGeneral,hamiltonTriGeneral]
totalPossibility= [madisonUniPossibility,madisonBiPossibility,madisonTriPossibility,hamiltonUniPossibility,hamiltonBiPossibility,hamiltonTriPossibility]

# The total word in the given dictionary is used to find the number of words.
def totalWords(my_dict):
    total=0
    for word in my_dict.keys():
        total += my_dict.get(word)
    return total

# computes the probability of generating the sentence generated
def totalSentencePossibility(sentenceWords):
    log_sum=0
    for word_prob in sentenceWords:
        log_sum += math.log(word_prob, 10)
    return log_sum

# calculate the total perplexity value of the test file.
def calculatePerplexity(sentenceWords,ngramPossibility):
    log_sum=0
    for word_prob in sentenceWords:
        log_sum = log_sum - math.log(word_prob, 2)
    return math.pow(2, log_sum / len(sentenceWords))
#calculates the frequency of words in the list and adds them in the dictionary.
def countUni(frequency,general):
    for i in range(0, len(general)):
        for item in general[i]:
            if (item in frequency):
                frequency[item] += 1
            else:
                frequency[item] = 1
#finds the total probability of words for unigram
def getUniPossibility(frequency,possibility):
    total = totalWords(frequency)
    for word in frequency.keys():
        poss = frequency.get(word) / total
        possibility[word] = poss
#finds the possibility of a pair of words for bigram. calculate the probability of the second word after the first.
def getBiPossibility(frequency,uniFrequency,possibility):
    for word in frequency.keys():
        words = word.split(" ")
        first_word = words[0]
        total = uniFrequency.get(first_word)
        poss = frequency.get(word) / total
        possibility[word] = poss
#calculates the probability of the third word coming after the first two words.
def getTriPossibility(frequency,biFrequency,possibility):
    for word in frequency.keys():
        words = word.split(" ")
        others = words[0] + " " + words[1]
        total = biFrequency.get(others)
        poss = frequency.get(word) / total
        possibility[word] = poss
#creates language model
def languageModel(s, n):
    s = s.lower()
    s = re.sub(r'[^a-zA-Z0-9]', ' ', s)
    tokens = [token for token in s.split(" ") if token != ""]
    ngrams = zip(*[tokens[i:] for i in range(n)])
    return [" ".join(ngram) for ngram in ngrams]
#read files and add them to required structures
def createAll():
    readText(hamiltonTexts,"h")
    readText(madisonTexts,"m")
    for i in range(6):
        countUni(totalFrequency[i],totalGeneral[i])
    for i in range(0,6,3):
        getUniPossibility(totalFrequency[i],totalPossibility[i])
    for i in range(1,6,3):
        getBiPossibility(totalFrequency[i],totalFrequency[i-1],totalPossibility[i])
    for i in range(2,6,3):
        getTriPossibility(totalFrequency[i],totalFrequency[i-1],totalPossibility[i])
#reads the files in the given file path
def readText(readList,author):
    for filename in readList:
        f = open(path + filename, "r")
        for line in f.readlines():
            if author == "m":
                madisonUniGeneral.append(languageModel(line, 1))
                madisonBiGeneral.append(languageModel(line, 2))
                madisonTriGeneral.append(languageModel(line, 3))
            else:
                hamiltonUniGeneral.append(languageModel(line, 1))
                hamiltonBiGeneral.append(languageModel(line, 2))
                hamiltonTriGeneral.append(languageModel(line, 3))

#creates a range of probabilities starting from zero to create a random sentence.
def countAllPossibility(my_dict):
    total=0.0000000
    sum_dict = {}
    for word in my_dict:
        poss = my_dict[word]
        total = total + float(poss)
        sum_dict[word]= total
    return total,sum_dict

#sorts the possibilities in the dictionary from small to large and transfers them to the list.
def sortDictionary(summaryDict):
    sortedDict = sorted(summaryDict.items(), key=lambda kv: kv[1])
    return sortedDict

#is an auxiliary function created to facilitate operations.
#If a word comes at the end of the sentence, it terminates the sentence creation and adds the point.
def countAndSort(introDict,ngram):
    fullPoss, sumDict = countAllPossibility(introDict)
    sortedArray = sortDictionary(sumDict)
    if ngram == 2 :
        if len(sortedArray) < 1:
            tempWord = "."
            tempPoss = 1.0
            return tempWord,tempPoss
        else:
            random_number = random.uniform(sortedArray[0][1], fullPoss)
            tempWord, tempPoss = rangeSearch(random_number, sortedArray, ngram)
            return tempWord, tempPoss
    elif ngram == 3:
        random_number = random.uniform(sortedArray[0][1], fullPoss)
        tempWord, tempPoss , LastTwoWords = rangeSearch(random_number, sortedArray, ngram)
        return tempWord, tempPoss , LastTwoWords
    else:
        random_number = random.uniform(0.0, fullPoss)
        tempWord,tempPoss = rangeSearch(random_number,sortedArray,ngram)
        return tempWord,tempPoss

#finds the range of random numbers generated to create the sentence. in doing so,
# it controls the values between the previous element and the current element.
# The probability of occurrence of words or phrases is the difference between the two elements.
# The function values for calculating the probabilities are prepared for this function.
def rangeSearch(number,myList,ngram):
    for i in range(0,len(myList)):
        if i+1 < len(myList):
            prevWord = myList[i]
            currentWord = myList[i + 1]
            if ngram == 1:
                if float(prevWord[1]) < number < float(currentWord[1]):
                    tempPoss = float(currentWord[1]) - float(prevWord[1])
                    return currentWord[0],tempPoss
            elif ngram == 2:
                if float(prevWord[1]) < number < float(currentWord[1]):
                    splittedPair = currentWord[0].split(" ")
                    firstWord = splittedPair[1]
                    tempPoss = float(currentWord[1]) - float(prevWord[1])
                    return firstWord,tempPoss
            elif ngram == 3:
                if float(prevWord[1]) < number < float(currentWord[1]):
                    splittedPair = currentWord[0].split(" ")
                    firstWord = splittedPair[2]
                    goToFindWord = " ".join([splittedPair[1],splittedPair[2]])
                    tempPoss = float(currentWord[1]) - float(prevWord[1])
                    return firstWord,tempPoss,goToFindWord
        else:
            if len(myList) == 1:
                if ngram == 1:
                    return  myList[0][0],float(myList[0][1])
                elif ngram == 2:
                    splittedPair = myList[0][0].split(" ")
                    firstWord = splittedPair[1]
                    tempPoss= myList[0][1]
                    return firstWord,tempPoss
                elif ngram == 3:
                    splittedPair = myList[0][0].split(" ")
                    firstWord = splittedPair[2]
                    tempPoss = myList[0][1]
                    lastTwoWords = " ".join([splittedPair[1],splittedPair[2]])
                    return firstWord,tempPoss , lastTwoWords

#creates unigram sentences. random number generation,
# finding the total probability, sorting the dictionary and printing the screen takes place here.
def generateUniGramSentences(toBeSorted):
    fullPosibility, summaryDict = countAllPossibility(toBeSorted)
    sortedArray = sortDictionary(summaryDict)
    sentencePossibility = []
    for i in range(0,30):
        random_number = random.uniform(0.0, fullPosibility)
        word,poss = rangeSearch(random_number,sortedArray,1)
        #Some errors would be exit. I didn't find source of errors. Please run again. Thank you.
        sys.stdout.write(word + " ")
        sentencePossibility.append(poss)
    print()
    print("Sentence Possibility:" + str(totalSentencePossibility(sentencePossibility)))


#creates bigram sentences. random number generation,
# finding the total probability, sorting the dictionary and printing the screen takes place here.
#the second dictionary is used to determine which word will come after the current word
def generateBiGramSentences(madeFrom,author):
    sentencePossibility = []
    secondDict = {}
    if author == "h":
        introUni = hamiltonUniPossibility
    else:
        introUni = madisonUniPossibility
    for i in range(0,29):
        if i == 0:
            initialWord,initialPoss = countAndSort(introUni,1)
            sys.stdout.write(initialWord + " ")
            sentencePossibility.append(initialPoss)
            secondDict = findNextWord(initialWord, madeFrom,1)
        newWord,wordPoss = countAndSort(secondDict,2)
        sys.stdout.write(str(newWord) + " ")
        sentencePossibility.append(wordPoss)
        secondDict = findNextWord(newWord,madeFrom,2)
    print()
    print("Sentence Possibility:" + str(totalSentencePossibility(sentencePossibility)))


#creates trigram sentences. random number generation,
#finding the total probability, sorting the dictionary and printing the screen takes place here.
#the second dictionary is used to determine which word will come after the current words
def generateTriGramSentences(madeFrom,author):
    sentencePossibility = []
    secondDict = {}
    if author == "h":
        introUni = hamiltonUniPossibility
        introBi = hamiltonBiPossibility
    else:
        introUni = madisonUniPossibility
        introBi = madisonBiPossibility
    for i in range(0,28):
        if i == 0:
            initialWord,initialPoss = countAndSort(introUni,1)
            sys.stdout.write(initialWord + " ")
            tempWord = initialWord
            sentencePossibility.append(initialPoss)
            secondDict = findNextWord(initialWord, introBi,2)
            initialTwoWord, secondPoss = countAndSort(secondDict,2)
            sys.stdout.write(str(initialTwoWord) + " ")
            tempWord = (tempWord + " " + initialTwoWord)
            sentencePossibility.append(secondPoss)
            secondDict = findNextWord(tempWord, madeFrom ,3)
        newWord, wordPoss , LastSecondWord = countAndSort(secondDict, 3)
        sys.stdout.write(str(newWord) + " ")
        sentencePossibility.append(wordPoss)
        secondDict = findNextWord(LastSecondWord, madeFrom, 3)
    print()
    print("Sentence Possibility:" + str(totalSentencePossibility(sentencePossibility)))

#calculates the probabilities of the next words and directs them to the corresponding functions.
def findNextWord(word,dict,ngram):
    tempDict = {}
    for pair in dict.keys():
        if ngram < 3 :
            splittedPair = pair.split(" ")
            firstWord = splittedPair[0]
            if word == firstWord:
                tempDict[pair] = dict.get(pair)
        else:
            splittedPair = pair.split(" ")
            firstWord = splittedPair[0]
            secondWord = splittedPair[1]
            firstTwoWords = " ".join([firstWord,secondWord])
            if word == firstTwoWords:
                tempDict[pair] = dict.get(pair)
    return tempDict

#used to read test files
#creates language model.
def readUnk(readList,ngram):
    for filename in readList:
        unknownBi =[]
        unknownTri =[]
        f = open(path + filename, "r")
        for line in f.readlines():
            unknownBi.append(languageModel(line,2))
            unknownTri.append(languageModel(line,3))
        if ngram == 2:
            totalUnknown.append(unknownBi)
        else:
            totalUnknown.append(unknownTri)

#calculates the complexity of sentences in test files and decides written by whom
def compareAndDetect(length,ngram):
    for i in range(0,length):
        if ngram == 3:
            hamiltonTotal = calculatePerplexity(hamiltonUnknown[i], hamiltonTriPossibility)
            madisonTotal = calculatePerplexity(madisonUnknown[i], madisonTriPossibility)
        else:
            hamiltonTotal = calculatePerplexity(hamiltonUnknown[i], hamiltonBiPossibility)
            madisonTotal = calculatePerplexity(madisonUnknown[i], madisonBiPossibility)
        if hamiltonTotal < madisonTotal:
            print("{}. Text Detection : Hamilton {} ".format(i+1,hamiltonTotal))
        else:
            print("{}. Text Detection : Madison {} ".format(i + 1, madisonTotal))
    hamiltonUnknown.clear()
    madisonUnknown.clear()
    totalUnknown.clear()

#calculate the probabilities of word or word pairs in test files. applies the smoothing process if not already available.
def detectAuthor(length,ngram):
    for i in range(0, len(totalUnknown)):
        hamiltonPoss = []
        madisonPoss = []
        for pair in totalUnknown[i][1]:
            hamiltonPair = hamiltonTriPossibility.get(pair)
            madisonPair = madisonTriPossibility.get(pair)
            if hamiltonPair == None:
                splittedPair = pair.split(" ")
                if ngram == 3:
                    firstTwoWords = " ".join([splittedPair[0], splittedPair[1]])
                    hamiltonPair = 1.0 / (hamiltonBiPossibility.get(firstTwoWords, 0) + len(hamiltonBiPossibility))
                else:
                    firstWord= splittedPair[0]
                    hamiltonPair = 1.0 / (hamiltonUniPossibility.get(firstWord, 0) + len(hamiltonUniPossibility))
            hamiltonPoss.append(hamiltonPair)
            if madisonPair == None:
                splittedPair = pair.split(" ")
                if ngram == 3:
                    firstTwoWords = " ".join([splittedPair[0], splittedPair[1]])
                    madisonPair = 1.0 / (madisonBiPossibility.get(firstTwoWords, 0) + len(madisonBiPossibility))
                else:
                    firstWord = splittedPair[0]
                    madisonPair = 1.0 / (madisonUniPossibility.get(firstWord, 0) + len(madisonUniPossibility))
            madisonPoss.append(madisonPair)
        hamiltonUnknown.append(hamiltonPoss)
        madisonUnknown.append(madisonPoss)
    compareAndDetect(length,ngram)


createAll()





#to print the output of all tasks on the console, call the function below. Thank you for reading.


def printAll():
    print("Unigram Language Model Example:")
    print(madisonUniGeneral[1])
    print("Bigram Language Model Example:")
    print(madisonBiGeneral[1])
    print("Trigram Language Model Example:")
    print(madisonTriGeneral[1])
    print("Hamilton Unigram 1:")
    generateUniGramSentences(hamiltonUniPossibility)
    print()
    print("Hamilton Unigram 2:")
    generateUniGramSentences(hamiltonUniPossibility)
    print()
    print("Madison Unigram 1:")
    generateUniGramSentences(madisonUniPossibility)
    print()
    print("Madison Unigram 2:")
    generateUniGramSentences(madisonUniPossibility)
    print()
    print("Hamilton Bigram 1:")
    generateBiGramSentences(hamiltonBiPossibility, "h")
    print()
    print("Hamilton Bigram 2:")
    generateBiGramSentences(hamiltonBiPossibility, "h")
    print()
    print("Madison Bigram 1:")
    generateBiGramSentences(madisonBiPossibility, "m")
    print()
    print("Madison Bigram 2:")
    generateBiGramSentences(madisonBiPossibility, "m")
    print()
    print("Hamilton Trigram 1:")
    generateTriGramSentences(hamiltonTriPossibility, "h")
    print()
    print("Hamilton Trigram 2:")
    generateTriGramSentences(hamiltonTriPossibility, "h")
    print()
    print("Madison Trigram 1:")
    generateTriGramSentences(madisonTriPossibility, "m")
    print()
    print("Madison Trigram 2:")
    generateTriGramSentences(madisonTriPossibility, "m")
    print()
    #magnitude of perplexity values can be different sometimes.
    print("For Text 9,11,12 with Bigram")
    readUnk(hamilton_Test, 2)
    detectAuthor(len(hamilton_Test), 2)
    print()
    print("For Text 47,48,58 with Bigram")
    readUnk(madison_Test, 2)
    detectAuthor(len(madison_Test), 2)
    print()
    print("For Unknown Texts with Bigram")
    readUnk(unknownTexts, 2)
    detectAuthor(len(unknownTexts), 2)
    print()
    # magnitude of perplexity values can be different sometimes.
    print("For Text 9,11,12 with Trigram")
    readUnk(hamilton_Test, 3)
    detectAuthor(len(hamilton_Test), 3)
    print()
    print("For Text 47,48,58 with Trigram")
    readUnk(madison_Test, 3)
    detectAuthor(len(madison_Test), 3)
    print()
    print("For Unknown Texts with Trigram")
    readUnk(unknownTexts, 3)
    detectAuthor(len(unknownTexts), 3)


#printAll()