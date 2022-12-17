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


barrels = {
    "commonNouns": [],
    "properNouns": [],
    "verbs": [],
    "adjectives": [],
    "adverbs": []
}


def lemmatizer(wordnet, pos_tags):
    # lemmatizer = wordnet
    keywords = []
    for i in pos_tags:
        if (i[1][0].lower() in ['n', 'v', 'a', 'r']):
            # print(i)
            keywords.append(wordnet.lemmatize(i[0], i[1][0].lower()))
            # keywords.append(wordnet.lemmatize(i))
        else:
            keywords.append(wordnet.lemmatize(i[0]))
    return keywords


def tokenize(wordnet, sentence):
    sentence_tokens = sentence.split(" ")
    pos_tags = nltk.pos_tag(sentence_tokens)
    # pos_tags = sentence_tokens

    keywords = lemmatizer(wordnet, pos_tags)
    # return keywords
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


def insertKeyword(dictionary, array, wordPos, power, currentPos):
    if (array[wordPos] in dictionary):
        # if(currentPos>=-1):
        # flag = False
        # counter = -1
        # for k in range(len(dictionary[array[wordPos]])):
        #     counter += 1
        # if (dictionary[array[wordPos]][k][0][1] == i):
        # cp = len(dictionary[array[wordPos]]) - 1
        if (currentPos > -1):
            dictionary[array[wordPos]][currentPos][0][2] += power
            dictionary[array[wordPos]][currentPos][1].append(wordPos)

            sorter(dictionary, array[wordPos], currentPos)

        else:
            dictionary[array[wordPos]].append(
                [[filename, i, power], [wordPos]])
        # flag = True
        # print(len(dictionary[array[wordPos]]) - counter)
        # break
        # if flag == False:
        # dictionary[array[wordPos]].append(
        #     [[filename, i, power], [wordPos]])

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
                              j, 5, tempDict[doc_list_title[j]])

        for j in range(len(doc_list_content)):
            if (doc_list_content[j] not in stop_words):
                if (doc_list_content[j] not in tempDict):
                    tempDict[doc_list_content[j]] = -1

                insertKeyword(keyword_dict, doc_list_content,
                              j, 1, tempDict[doc_list_content[j]])


keyword_dict_json = json.dumps(keyword_dict, indent=1)
print("Done")

end = time.perf_counter()
# find elapsed time in seconds
ms = (end-start)
print(f"Elapsed {ms:.03f}  secs.")


with open("tempX.json", "w") as myFile:
    myFile.write(keyword_dict_json)
