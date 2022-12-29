import re  # used to remove punctuation and special characters
from nltk.corpus import stopwords
import nltk
import json
import time
from pathlib import Path
from nltk.stem import WordNetLemmatizer
wordnet = WordNetLemmatizer()

# Declare root path and note all the present files in the dataset
root = Path('./Dataset/newsdata')
file_objs = root.iterdir()
files = []
for i in file_objs:
    files.append(str(i))


def lemmatizer(wordnet, pos_tags):
    keywords = []
    for i in pos_tags:
        keywords.append(wordnet.lemmatize(i))
    return keywords


def tokenize(wordnet, sentence):
    sentence_tokens = sentence.split(" ")
    pos_tags = sentence_tokens
    keywords = lemmatizer(wordnet, pos_tags)
    # keywords = pos_tags
    return keywords


def sorter(dictionary, key, wordDocIntersection):
    if (wordDocIntersection == len(dictionary[key])):
        return

    temp2 = len(dictionary[key]) - wordDocIntersection[key]
    while (temp2 > 1 and float(dictionary[key][temp2 - 1][0][1]) < float(dictionary[key][temp2][0][1])):
        if (key == "Covid-19"):
            pass
        temp = dictionary[key][temp2 - 1]
        dictionary[key][temp2 -
                        1] = dictionary[key][temp2]
        dictionary[key][temp2] = temp
        wordDocIntersection[key] += 1
        temp2 = len(dictionary[key]) - wordDocIntersection[key]


def forwardIndexer(files, fileNum=0):

    # create stopwords list
    stop_words = stopwords.words('english')
    stop_words.extend(['@', '\u2014', '.'])
    # Declare empty dictionary and populate it
    forwardIndex = {}
    for file in files:  # adjust this for filename
        # filename = (file.split('\\')[2])[:-5]
        filee = open(file)
        json_data = json.load(filee)
        print(f"{file} started")
        fileNum += 1

        for i in range(len(json_data)):

            # data = json_data[i]['title']+" "+json_data[i]['content']
            data = json_data[i]['title']+" !369257! "+json_data[i]['content']

            # clean_string = re.sub(r'[^\w\s]', '', data)

            # doc_list = tokenize(wordnet, clean_string)
            doc_list = tokenize(wordnet, data)

            docID = int(str(fileNum)+str(i))

            forwardIndex[docID] = []
            for j in range(len(doc_list)):
                # duplication is allowed in forward index
                if (doc_list[j] not in stop_words):
                    forwardIndex[docID].append(doc_list[j])
    return forwardIndex


def invertedIndexer(forwardIndex, reverseIndex={}):
    for doc in forwardIndex:
        wordPosition = 0
        titleLength = 0
        for i in range(len(forwardIndex[doc])):
            titleLength += 1
            if (forwardIndex[doc][i] == "!369257!"):
                break
        # titleLength = 7  # making the assumption of a 7 length title
        counter = 0  # ^
        wordDocIntersection = {}
        totalWords = len(forwardIndex[doc])

        for word in forwardIndex[doc]:
            if (word not in wordDocIntersection):
                wordDocIntersection[word] = 1

            if (counter < titleLength):
                power = 5
            else:
                power = 1 / totalWords
            counter += 1
            if (word not in reverseIndex):
                reverseIndex[word] = [[[doc, str(power)], [wordPosition]]]
            else:
                if (reverseIndex[word][len(reverseIndex[word])-wordDocIntersection[word]][0][0] == doc):
                    fltPower = float(reverseIndex[word][len(
                        reverseIndex[word]) - wordDocIntersection[word]][0][1])
                    fltPower += power
                    reverseIndex[word][len(reverseIndex[word]) - wordDocIntersection[word]][0][1] = str(reverseIndex[word][len(
                        reverseIndex[word]) - wordDocIntersection[word]][0][1])
                    reverseIndex[word][len(reverseIndex[word]) -
                                       wordDocIntersection[word]][1].append(wordPosition)
                else:
                    reverseIndex[word].append(
                        [[doc, str(power)], [wordPosition]])

                sorter(reverseIndex, word, wordDocIntersection)

            wordPosition += 1
    return reverseIndex


def addDoc(doc):

    fIndex = forwardIndexer(doc, 5)
    # Open existing forward index and modify it
    ogForwardIndex = json.load(open("forwardIndexLARGE.json"))
    ogForwardIndex.append(fIndex)
    newForwardIndex = json.dumps(ogForwardIndex, indent=2)
    with open("forwardIndexLARGE.json", "w") as myFile:
        myFile.write(newForwardIndex)

    # Open existing inverted index and mofify it
    ogInvertedIndex = json.load(open("invertedIndexLARGE.json"))
    invertedIndexer(fIndex, ogInvertedIndex)
    newInvertedIndex = json.dumps(ogInvertedIndex, indent=2)
    with open("invertedIndexLARGE.json", "w") as myFile:
        myFile.write(newInvertedIndex)


start = time.perf_counter()

forwardIndex = forwardIndexer(files)


end = time.perf_counter()
ms = (end-start)
print(f"Forward index Elapsed {ms:.03f}  secs.")

forwardIndexJSON = json.dumps(forwardIndex, indent=2)
with open("forwardIndexSmol.json", "w") as myFile:
    myFile.write(forwardIndexJSON)

forwardIndex = json.load(open("forwardIndexSmol.json"))


reverseIndex = invertedIndexer(forwardIndex)


reverseIndexJSON = json.dumps(reverseIndex, indent=2)

end = time.perf_counter()
ms = (end-start)
print(f"Elapsed {ms:.03f}  secs.")

with open("invertedIndexSmol.json", "w") as myFile:
    myFile.write(reverseIndexJSON)
