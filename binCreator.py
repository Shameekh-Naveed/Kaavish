import nltk

nltk.download("stopwords")
nltk.download("wordnet")
nltk.download("averaged_perceptron_tagger")

from nltk.stem import WordNetLemmatizer
from pathlib import Path
import json

# loat the inverted index file into memory
# run the forRevIndex.py file to generate the inverted index file
reverseData = json.load(open("invertedIndex4.json", "r"))

wordnet = WordNetLemmatizer()

# list of all the words in the dictionary
reverseKeys = list(reverseData.keys())

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
        binData[taggedKey[1]][taggedKey[0]] = reverseData[taggedKey[0]]
    else:
        binData[taggedKey[1]] = {}
        binData[taggedKey[1]][taggedKey[0]] = reverseData[taggedKey[0]]


# save the binData to a separate files
for tag in binData:
    with open("binData_" + tag + ".json", "w") as f:
        json.dump(binData[tag], f)
