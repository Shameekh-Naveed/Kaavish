import nltk
import json
import time
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from pathlib import Path
wordnet = WordNetLemmatizer()


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
    return keywords


def sorter(dictionary, key, listPos):
    if (listPos == 0):
        return

    i = listPos

    while (i > 0 and dictionary[key][i][0][2] > dictionary[key][i-1][0][2]):
        temp = dictionary[key][i-1][0][2]
        dictionary[key][i-1][0][2] = dictionary[key][i][0][2]
        dictionary[key][i][0][2] = temp
        i -= 1

    listPos = i - 1


def insertKeyword(dictionary, array, wordPos, power):
    if (array[wordPos] in dictionary):
        flag = False
        counter = -1
        for k in range(len(dictionary[array[wordPos]])):
            counter += 1
            if (dictionary[array[wordPos]][k][0][1] == i):

                dictionary[array[wordPos]][k][0][2] += power
                dictionary[array[wordPos]][k][1].append(wordPos)
                flag = True
                break
        if flag == False:
            dictionary[array[wordPos]].append(
                [[filename, i, power], [wordPos]])
        sorter(dictionary, array[wordPos], counter)

    else:
        # append the new word to the keyword list
        # keyword_list.append(array[wordPos])

        # create a new entry in the dictionary
        dictionary[array[wordPos]] = []

        # append the document number and the position of the keyword in the document in a list
        # separately
        dictionary[array[wordPos]].append([[filename, i, power], [wordPos]])


# create stopwords list
stop_words = stopwords.words('english')
stop_words.extend(['@', '\u2014', '.'])


keyword_dict = {}
start = time.perf_counter()


for file in files:
    filename = file.split('\\')[2]
    filee = open(file)
    json_data = json.load(filee)
    print(f"{file} started")

    for i in range(len(json_data)):  # i is the document number/ID

        doc_list_title = tokenize(wordnet, json_data[i]['title'])
        doc_list_content = tokenize(wordnet, json_data[i]['content'])

        tempDict = {}

        for j in range(len(doc_list_title)):
            if (doc_list_title[j] not in stop_words):
                if (doc_list_title[j] not in tempDict):
                    tempDict[doc_list_title[j]] = -1

                insertKeyword(keyword_dict, doc_list_title,
                              j, 5)

        for j in range(len(doc_list_content)):
            if (doc_list_content[j] not in stop_words):
                if (doc_list_content[j] not in tempDict):
                    tempDict[doc_list_content[j]] = -1

                insertKeyword(keyword_dict, doc_list_content,
                              j, 1)


keyword_dict_json = json.dumps(keyword_dict, indent=1)
print("Done")

end = time.perf_counter()
# find elapsed time in seconds
ms = (end-start)
print(f"Elapsed {ms:.03f}  secs.")


with open("reverseIndex.json", "w") as myFile:
    myFile.write(keyword_dict_json)
