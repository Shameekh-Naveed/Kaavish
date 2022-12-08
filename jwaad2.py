import nltk
import json
from nltk.stem import WordNetLemmatizer
import pickle
import time 

class docData:
    def __init__(self, id,position):
        self.id = id
        self.position = [position]
    
    def addPosition(self,pos):
        self.position.append(pos)

    def getId(self):
        return self.id


class wordData:
    def __init__(self, name):
        self.name = name
        self.frequency = 0
        self.docList = []  # list of docDatas
    
    def addDocument(self, docId, pos):
        self.frequency+=1
        flag = 0 # check if document already exists
        for doc in self.docList:
            if(doc.getId == docId):
                doc.position.append(pos)
                flag = 1 # doc does exist
                break
        if(flag == 0) : # doc did not exist
            self.docList.append(docData(docId,pos))


# start = time.time_ns()
start = time.perf_counter()

# nltk.download('punkt')
# nltk.download('omw-1.4')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')


def stopWords_remmover_and_lemmatizer(pos_tags):
    lemmatizer = WordNetLemmatizer()
    required = ['n', 'v', 'r', 'a']
    keywords = []
    for i in pos_tags:
        if (i[1][0].lower() in required):
            keywords.append(lemmatizer.lemmatize(i[0], i[1][0].lower()))
    return keywords


def tokenize(sentence):
    sentence_tokens = nltk.word_tokenize(sentence.lower())
    # print(sentence_tokens)
    pos_tags = nltk.pos_tag(sentence_tokens)
    # print(pos_tags)
    keywords = stopWords_remmover_and_lemmatizer(pos_tags)
    return keywords
    # return sentence_tokens


file = open('buzzfeed.json')

json_data = json.load(file)


# keyword_list = []
keyword_dict = [] # list of wordData
temp = 1

for i in range(len(json_data)):
    wordList = tokenize(json_data[i]['title'])
    kFlag = 0
    for word in wordList:
        for keyWord in keyword_dict:
            if (keyWord.name == word):
                keyWord.addDocument(i,temp)
                temp+=1
                kFlag = 1
                break
        if (kFlag == 0):
            new = wordData(word)
            new.addDocument(i,temp)
            keyword_dict.append(new)
        
    # print(doc_list)
    

print("done")

# keyword_dict_json = json.dumps(keyword_dict, indent=4)
# keyword_dict_json = json.dumps(keyword_dict, indent=4)


# with open("reverseIndex.json", "w") as myFile:
    # myFile.write(keyword_dict_json)

with open('file.pkl', 'wb') as file:
      
    # A new file will be created
    pickle.dump(keyword_dict, file)


end = time.perf_counter()
# find elapsed time in seconds
ms = (end-start) * 10**6
print(f"Elapsed {ms:.03f} micro secs.")
