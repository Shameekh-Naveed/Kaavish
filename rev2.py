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
    # keywords = lemmatizer(wordnet, pos_tags)
    keywords = pos_tags
    return keywords


# create stopwords list
stop_words = stopwords.words('english')
stop_words.extend(['@', '\u2014', '.'])
# Decflare empty dictionary and populate it
forwardIndex = {}

start = time.perf_counter()

for file in files:  # adjust this for filename
    filename = file.split('\\')[2]
    filee = open(file)
    json_data = json.load(filee)
    print(f"{file} started")

    for i in range(len(json_data)):

        data = json_data[i]['title']+" "+json_data[i]['content']
        # clean_string = re.sub(r'[^\w\s]', '', data)

        # doc_list = tokenize(wordnet, clean_string)
        doc_list = tokenize(wordnet, data)

        forwardIndex[i] = []
        for j in range(len(doc_list)):
            # duplication is allowed in forward index
            if (doc_list[j] not in stop_words):
                forwardIndex[i].append(doc_list[j])


forwardIndexJSON = json.dumps(forwardIndex, indent=2)
with open("findextemp.json", "w") as myFile:
    myFile.write(forwardIndexJSON)

forwardIndex = json.load(open("findextemp.json"))


reverseIndex = {}

tempVar = 0
tempList = []
for doc in forwardIndex:
    filename = power = 0  # make way for power and filename
    wordPosition = 0
    for word in forwardIndex[doc]:
        if (word in reverseIndex):
            if (reverseIndex[word][len(reverseIndex[word])-1][0][1] == doc):
                reverseIndex[word][len(reverseIndex[word])-1][0][2] += 1
                reverseIndex[word][len(reverseIndex[word])-1][1].append(wordPosition)
            else:
                reverseIndex[word].append([[filename, doc, power], [wordPosition]])
        else:
            reverseIndex[word] = [[[filename, doc, power], [wordPosition]]]
        wordPosition+=1
        


reverseIndexJSON = json.dumps(reverseIndex, indent=2)

end = time.perf_counter()
# find elapsed time in seconds
ms = (end-start)
print(f"Elapsed {ms:.03f}  secs.")

with open("temp.json", "w") as myFile:
    myFile.write(reverseIndexJSON)
