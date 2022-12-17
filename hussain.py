import json
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import time
start = time.perf_counter()
ps = PorterStemmer()
#opening a json file
json_file_object = open("Dataset/newsdata/cbsnews.json", "r")

#loading json file as python dictionary
data = json.load(json_file_object)

stop = stopwords.words('english')
stop.extend(['@','a','the','an',";","of"])

def forward_indexing(documents):
    forward_index = {}
    for i in range(len(documents)):
        words = documents[i]['content'].split()
        words2 = []
        for word in words:
            if word not in stop:
                word = ps.stem(word)
                words2.append(word)
        forward_index[i] = words2
    return forward_index

def inverted_indexing(documents):
    forward_index = forward_indexing(documents)
    inverted_index = {}
    for doc_id, words in forward_index.items():
        for word in words:
            if word not in inverted_index:
                inverted_index[word] = [doc_id]
            else:
                inverted_index[word].append(doc_id)
    return inverted_index

inverted_indexing(data)
end = time.perf_counter()
print(end-start)