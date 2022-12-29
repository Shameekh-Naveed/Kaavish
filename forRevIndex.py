import re  # used to remove punctuation and special characters
from nltk.corpus import stopwords
import nltk
import json
import time
from pathlib import Path
from nltk.stem import WordNetLemmatizer


wordnet = WordNetLemmatizer()

# Declare root path and note all the present files in the dataset
root = Path("./Dataset/newsdata")
file_objs = root.iterdir()
files = []
for i in file_objs:
    files.append(str(i))


def lemmatizer(wordnet, pos_tags):
    keywords = []
    useful_tags = ["N", "R", "V", "J"]
    for i in pos_tags:
        if i[1][0] in useful_tags:
            if i[1][0] == "J":
                keywords.append(wordnet.lemmatize(i[0], pos="a"))
            else:
                keywords.append(wordnet.lemmatize(i[0], pos=i[1][0].lower()))
        else:
            keywords.append(wordnet.lemmatize(i[0]))
    return keywords

def tokenize(wordnet, sentence):
    wordList = sentence.split(" ")
    keywords = lemmatizer(wordnet, nltk.pos_tag(wordList))
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
    stop_words = stopwords.words("english")
    stop_words.extend(["@", "\u2014", "."])
    # Declare empty dictionary and populate it
    forwardIndex = {}

    for file in files:  # adjust this for filename
        filee = open(file)
        json_data = json.load(filee)
        print(f"{file} started")
        fileNum += 1

        for i in range(len(json_data)):

            data = json_data[i]["title"] + " " + json_data[i]["content"]
            clean_string = re.sub(r"[^\w\s]", "", data)

            doc_list = tokenize(wordnet, clean_string)
            # doc_list = tokenize(wordnet, data)

            docID = int(str(fileNum) + str(i))

            forwardIndex[docID] = []
            for j in range(len(doc_list)):
                # duplication is allowed in forward index
                if doc_list[j] not in stop_words:
                    forwardIndex[docID].append(doc_list[j])

            if i == 1000:
                print("km pay gya")
                break

    return forwardIndex

def invertedIndexer(forwardIndex, reverseIndex={}):
    for doc in forwardIndex:
        wordPosition = 0
        titleLength = 0
        for i in range(len(forwardIndex[doc])):
            titleLength += 1
            if forwardIndex[doc][i] == "!369257!":
                break

        counter = 0  # ^
        wordDocIntersection = {}

        totalWords = len(forwardIndex[doc])
        for word in forwardIndex[doc]:
            if word not in wordDocIntersection:
                wordDocIntersection[word] = 1

            if counter < titleLength:
                power = 5

            else:
                power = 1 / totalWords
            counter += 1
            if word not in reverseIndex:
                reverseIndex[word] = [[[doc, power], [wordPosition]]]
            else:
                if (
                    reverseIndex[word][
                        len(reverseIndex[word]) - wordDocIntersection[word]
                    ][0][0]
                    == doc
                ):
                    fltPower = float(
                        reverseIndex[word][
                            len(reverseIndex[word]) - wordDocIntersection[word]
                        ][0][1]
                    )
                    fltPower += power
                    reverseIndex[word][
                        len(reverseIndex[word]) - wordDocIntersection[word]
                    ][0][1] = str(
                        reverseIndex[word][
                            len(reverseIndex[word]) - wordDocIntersection[word]
                        ][0][1]
                    )
                    reverseIndex[word][
                        len(reverseIndex[word]) - wordDocIntersection[word]
                    ][1].append(wordPosition)
                else:
                    reverseIndex[word].append([[doc, str(power)], [wordPosition]])

                sorter(reverseIndex, word, wordDocIntersection)

            wordPosition += 1
    return reverseIndex

def addDoc(doc):
    list = [doc]
    fIndex = forwardIndexer(list, 5)
    # Open existing forward index and modify it
    ogForwardIndex = json.load(open("FIndexJ.json"))
    ogForwardIndex.update(fIndex)
    newForwardIndex = json.dumps(ogForwardIndex, indent=2)
    with open("FIndexJ.json", "w") as myFile:
        myFile.write(newForwardIndex)

    # Open existing inverted index and mofify it
    ogInvertedIndex = json.load(open("RIndexJ.json"))
    newInvertedIndex = invertedIndexer(fIndex, ogInvertedIndex)
    newInvertedIndex = json.dumps(ogInvertedIndex, indent=2)
    with open("RIndexJ.json", "w") as myFile:
        myFile.write(newInvertedIndex)


start = time.perf_counter()

# forwardIndex = forwardIndexer(files)

addDoc("./Dataset/newsdata/disclosetv.json")

forwardIndexJSON = json.dumps(forwardIndex, indent=2)
with open("FIndexJ.json", "w") as myFile:
    myFile.write(forwardIndexJSON)

forwardIndex = json.load(open("FIndexJ.json"))


reverseIndex = invertedIndexer(forwardIndex)


reverseIndexJSON = json.dumps(reverseIndex, indent=2)

# BIN CREATION

# list of all the words in the dictionary
reverseKeys = list(reverseIndex.keys())

taggedKeys = nltk.pos_tag(reverseKeys)

binData = {}

# format :
# {
#     "NN": {
#         "word1": [doc1, doc2, doc3],
#         "word2": [doc1, doc2, doc3],
#         "word3": [doc1, doc2, doc3],
#     }
# }

for taggedKey in taggedKeys:
    if taggedKey[1] in binData:
        binData[taggedKey[1]][taggedKey[0]] = reverseIndex[taggedKey[0]]
    else:
        binData[taggedKey[1]] = {}
        binData[taggedKey[1]][taggedKey[0]] = reverseIndex[taggedKey[0]]


end = time.perf_counter()
# find elapsed time in seconds
ms = end - start
print(f"Elapsed {ms:.03f}  secs.")

with open("RIndexJ.json", "w") as myFile:
    myFile.write(reverseIndexJSON)

# save the binData to a separate files
for tag in binData:
    with open("./barrels/Bin_" + tag + ".json", "w") as f:
        json.dump(binData[tag], f)
