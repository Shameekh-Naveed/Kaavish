import re  # used to remove punctuation and special characters
from nltk.corpus import stopwords
import nltk
import json
import time
from pathlib import Path
from nltk.stem import WordNetLemmatizer

# nltk.download("stopwords")
# nltk.download("wordnet")
# nltk.download("averaged_perceptron_tagger")

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
    keywords = lemmatizer(wordnet, nltk.pos_tag(nltk.word_tokenize(sentence)))
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
        clean_string = re.sub(r"[^\w\s]", "", data)

        doc_list = tokenize(wordnet, clean_string)
        # doc_list = tokenize(wordnet, data)

        docID = int(str(fileNum) + str(i))

        forwardIndex[docID] = []
        for j in range(len(doc_list)):
            # duplication is allowed in forward index
            if doc_list[j] not in stop_words:
                forwardIndex[docID].append(doc_list[j])

        if i == 50:
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
            wordDocIntersection[word.lower()] = 1

        if counter < titleLength:
            power = 5
        else:
            power = 1
        counter += 1
        if word not in reverseIndex:
            reverseIndex[word.lower()] = [[[doc, power], [wordPosition]]]
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

# BIN CREATION

# list of all the words in the dictionary
reverseKeys = list(reverseIndex.keys())

taggedKeys = nltk.pos_tag(reverseKeys)

binData = {}

# new format :
# {
#     "NN": {
#         "a": {
#             "word1": [doc1, doc2, doc3]
#         }
# }
# }

for taggedKey in taggedKeys:
    # print(taggedKey)
    if taggedKey[1] in binData:
        if taggedKey[0][0] in binData[taggedKey[1]]:
            binData[taggedKey[1]][taggedKey[0][0]][taggedKey[0]] = reverseIndex[
                taggedKey[0]
            ]
        else:
            binData[taggedKey[1]][taggedKey[0][0]] = {}
            binData[taggedKey[1]][taggedKey[0][0]][taggedKey[0]] = reverseIndex[
                taggedKey[0]
            ]

    else:
        binData[taggedKey[1]] = {}
        binData[taggedKey[1]][taggedKey[0][0]] = {}
        binData[taggedKey[1]][taggedKey[0][0]][taggedKey[0]] = reverseIndex[
            taggedKey[0]
        ]

# print(binData)
end = time.perf_counter()
# find elapsed time in seconds
ms = end - start
print(f"Elapsed {ms:.03f}  secs.")

with open("invertedIndex4.json", "w") as myFile:
    myFile.write(reverseIndexJSON)

# save the binData to a separate files
Path("bins").mkdir(parents=True, exist_ok=True)

print("Saving bins to files")
for tag in binData:
    pos_folder = "bins/" + tag

    Path(pos_folder).mkdir(parents=True, exist_ok=True)

    for alphabet in binData[tag]:

        alphabet_file = pos_folder + "/" + alphabet + ".json"

        with open(alphabet_file, "w") as f:
            json.dump(binData[tag][alphabet], f)
            f.close()
print("Done")
