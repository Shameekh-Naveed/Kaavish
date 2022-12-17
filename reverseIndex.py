import nltk
import json
import time
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from pathlib import Path

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

start = time.perf_counter()


def lemmatizer(pos_tags):
    lemmatizer = WordNetLemmatizer()
    keywords = []
    for i in pos_tags:
        if (i[1][0].lower() in ['n', 'v', 'a', 'r']):
            # print(i)
            keywords.append(lemmatizer.lemmatize(i[0], i[1][0].lower()))
        else:
            keywords.append(lemmatizer.lemmatize(i[0]))
    return keywords


def tokenize(sentence):
    sentence_tokens = nltk.word_tokenize(sentence.lower())
    pos_tags = nltk.pos_tag(sentence_tokens)

    keywords = lemmatizer(pos_tags)
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


# keyword_list = []
# keyword_dict = {}

keyword_dict = {}


for file in files:
    filename = file.split('\\')[2]
    filee = open(file)
    json_data = json.load(filee)
    print(f"{file} started")
    if("conspiracy" not in filename):
        continue

    # keyword_list = []
    # keyword_dict = {}

    for i in range(len(json_data)):  # i is the document number/ID
        doc_list_title = tokenize(json_data[i]['title'])
        doc_list_content = tokenize(json_data[i]['content'])

        for j in range(len(doc_list_title)):
            if (doc_list_title[j] not in stop_words):
                insertKeyword(keyword_dict, doc_list_title, j, 2)

        for j in range(len(doc_list_content)):
            if (doc_list_content[j] not in stop_words):
                insertKeyword(keyword_dict, doc_list_content, j, 0.5)

        # if (i == 100):
        #     break


keyword_dict_json = json.dumps(keyword_dict, indent=1)
print("Done")

end = time.perf_counter()
# find elapsed time in seconds
ms = (end-start)
print(f"Elapsed {ms:.03f}  secs.")


with open("temp3.json", "w") as myFile:
    myFile.write(keyword_dict_json)
