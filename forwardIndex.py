import nltk
import json
import time
from pathlib import Path
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import re  # used to remove punctuation and special characters

start = time.perf_counter()


def lemmatizer(pos_tags):
    lemmatizer = WordNetLemmatizer()
    keywords = []
    for i in pos_tags:
        if (i[1][0].lower() in ['n', 'v', 'a', 'r']):
            keywords.append(lemmatizer.lemmatize(i[0], i[1][0].lower()))
        else:
            keywords.append(lemmatizer.lemmatize(i[0]))
    return keywords


def tokenize(sentence):
    sentence_tokens = nltk.word_tokenize(sentence.lower())
    pos_tags = nltk.pos_tag(sentence_tokens)
    # keywords = lemmatizer(pos_tags)
    keywords = sentence.split(" ")
    return keywords

# Declare root path and note all the present files in the dataset
root = Path('./Dataset/newsdata')
file_objs = root.iterdir()
files = []
for i in file_objs:
    files.append(str(i))



# create stopwords list
stop_words = stopwords.words('english')
stop_words.extend(['@', '\u2014', '.'])


# Decflare empty dictionary and populate it
keyword_dict = {}

for file in files:
    filename = file.split('\\')[2]
    filee = open(file)
    json_data = json.load(filee)
    print(f"{file} started")

    if ("cbsnews" not in filename):
        continue

    for i in range(len(json_data)):

        data = json_data[i]['title']+" "+json_data[i]['content']
        clean_string = re.sub(r'[^\w\s]', '', data)

        doc_list = tokenize(clean_string)

        keyword_dict[i] = []
        for j in range(len(doc_list)):
            # duplication is allowed in forward index
            if (doc_list[j] not in stop_words):
                keyword_dict[i].append(doc_list[j])

        if(i == 1000):
            break
        # print(f"Document {i} done")
        
        

keyword_dict_json = json.dumps(keyword_dict, indent=2)
end = time.perf_counter()
# find elapsed time in seconds
ms = (end-start)
print(f"Elapsed {ms:.03f}  secs.")

with open("forward.json", "w") as myFile:
    myFile.write(keyword_dict_json)
