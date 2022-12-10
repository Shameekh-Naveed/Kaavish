import nltk
import json
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

def lemmatizer(pos_tags):
    lemmatizer = WordNetLemmatizer()
    required = ['n','a', 'v', 'r']
    keywords = []
    for i in pos_tags:
        if (i[1][0].lower() in required):
            keywords.append(lemmatizer.lemmatize(i[0],i[1][0].lower()))
    return keywords



def tokenize(sentence):
    sentence_tokens = nltk.word_tokenize(sentence.lower())
    pos_tags = nltk.pos_tag(sentence_tokens)
    
    keywords = lemmatizer(pos_tags)
    return keywords

# create stopwords list
stop_words = stopwords.words('english')
stop_words.extend(['@', '\u2014', '.'])


# open file
file = open('bbc.json')
json_data = json.load(file)


keyword_list = []
keyword_dict = {}

for i in range(len(json_data)):
    doc_list = tokenize(json_data[i]['title']+" "+json_data[i]['content'])
    for j in doc_list:
      if(j not in keyword_dict and j not in stop_words):
        keyword_list.append(j)
        keyword_dict[j] = []
        keyword_dict[j].append((i,doc_list.count(j)))
      elif(j in keyword_dict):
        keyword_dict[j].append((i,doc_list.count(j)))
    print(f"Document {i} done")
    if (i==500):
        break

keyword_dict_json = json.dumps(keyword_dict, indent=1)
print("Done")

with open("reverse.json","w") as myFile:
    myFile.write(keyword_dict_json)
    