import re  # used to remove punctuation and special characters
from nltk.corpus import stopwords
import nltk
import json
import time
from pathlib import Path
from nltk.stem import WordNetLemmatizer

nltk.download("stopwords")
nltk.download("wordnet")


wordnet = WordNetLemmatizer()

# Declare root path and note all the present files in the dataset
root = Path("./Dataset/newsdata")
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
    if wordDocIntersection == len(dictionary[key]):
        return

    temp2 = len(dictionary[key]) - wordDocIntersection[word]
    while temp2 > 1 and dictionary[key][temp2 - 1][0][1] < dictionary[key][temp2][0][1]:
        if key == "Covid-19":
            pass
        temp = dictionary[key][temp2 - 1]
        dictionary[key][temp2 - 1] = dictionary[key][temp2]
        dictionary[key][temp2] = temp
        wordDocIntersection[word] += 1
        temp2 = len(dictionary[key]) - wordDocIntersection[word]


# create stopwords list
stop_words = stopwords.words("english")
stop_words.extend(["@", "\u2014", "."])
# Declare empty dictionary and populate it
forwardIndex = {}

# Dataset/newsdata/abcnews.json


start = time.perf_counter()
fileNum = 0

for file in files:  # adjust this for filename
    # filename = (file.split("\\")[2])[:-5] # for windows
    filename = (file.split("/")[2])[:-5]  # for linux

    filee = open(file)
    json_data = json.load(filee)
    print(f"{file} started")
    fileNum += 1

    for i in range(len(json_data)):

        data = json_data[i]["title"] + " " + json_data[i]["content"]
        # clean_string = re.sub(r'[^\w\s]', '', data)

        # doc_list = tokenize(wordnet, clean_string)
        doc_list = tokenize(wordnet, data)

        docID = int(str(fileNum) + str(i))

        forwardIndex[docID] = []
        for j in range(len(doc_list)):
            # duplication is allowed in forward index
            if doc_list[j] not in stop_words:
                forwardIndex[docID].append(doc_list[j])

        if i == 1000:
            print("km pay gya")
            break


forwardIndexJSON = json.dumps(forwardIndex, indent=2)
with open("findextemp3.json", "w") as myFile:
    myFile.write(forwardIndexJSON)

forwardIndex = json.load(open("findextemp3.json"))


reverseIndex = {}

tempVar = 0
tempList = []

# inverted Index

for doc in forwardIndex:
    power = 1  # make way for power and
    wordPosition = 0
    titleLength = 7  # making the assumption of a 7 length title
    counter = 0  # ^
    wordDocIntersection = {}
    for word in forwardIndex[doc]:
        if word not in wordDocIntersection:
            wordDocIntersection[word] = 1

        if counter < titleLength:
            power = 5
        else:
            power = 1
        counter += 1
        if word not in reverseIndex:
            reverseIndex[word] = [[[doc, power], [wordPosition]]]
        else:
            if (
                reverseIndex[word][len(reverseIndex[word]) - wordDocIntersection[word]][
                    0
                ][0]
                == doc
            ):
                reverseIndex[word][len(reverseIndex[word]) - wordDocIntersection[word]][
                    0
                ][1] += power
                reverseIndex[word][len(reverseIndex[word]) - wordDocIntersection[word]][
                    1
                ].append(wordPosition)
            else:
                reverseIndex[word].append([[doc, power], [wordPosition]])

            sorter(reverseIndex, word, wordDocIntersection)

        wordPosition += 1


reverseIndexJSON = json.dumps(reverseIndex, indent=2)

end = time.perf_counter()
# find elapsed time in seconds
ms = end - start
print(f"Elapsed {ms:.03f}  secs.")

with open("invertedIndex4.json", "w") as myFile:
    myFile.write(reverseIndexJSON)
