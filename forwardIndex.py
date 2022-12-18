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
    return keywords


# create stopwords list
stop_words = stopwords.words('english')
stop_words.extend(['@', '\u2014', '.'])
# Decflare empty dictionary and populate it
keyword_dict = {}

start = time.perf_counter()

for file in files:
    filename = file.split('\\')[2]
    filee = open(file)
    json_data = json.load(filee)
    print(f"{file} started")

    for i in range(len(json_data)):

        data = json_data[i]['title']+" "+json_data[i]['content']
        clean_string = re.sub(r'[^\w\s]', '', data)

        doc_list = tokenize(wordnet, clean_string)

        keyword_dict[i] = []
        for j in range(len(doc_list)):
            # duplication is allowed in forward index
            if (doc_list[j] not in stop_words):
                keyword_dict[i].append(doc_list[j])


keyword_dict_json = json.dumps(keyword_dict, indent=2)
end = time.perf_counter()
# find elapsed time in seconds
ms = (end-start)
print(f"Elapsed {ms:.03f}  secs.")

with open("forwardIndex.json", "w") as myFile:
    myFile.write(keyword_dict_json)
