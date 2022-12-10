import nltk
import json
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import re #used to remove punctuation and special characters

def lemmatizer(pos_tags):
    lemmatizer = WordNetLemmatizer()
    keywords = []
    for i in pos_tags:
        if(i[1][0].lower() in ['n','v','a','r']):
            keywords.append(lemmatizer.lemmatize(i[0],i[1][0].lower()))
        else:
            keywords.append(lemmatizer.lemmatize(i[0]))
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

keyword_dict = {}

for i in range(len(json_data)):
    
    data = json_data[i]['title']+" "+json_data[i]['content']
    clean_string = re.sub(r'[^\w\s]','',data)

    doc_list = tokenize(clean_string)

    keyword_dict[i] = []
    for j in range(len(doc_list)):
        # duplication is allowed in forward index
        if(doc_list[j] not in stop_words):
            keyword_dict[i].append(doc_list[j])
        
    print(f"Document {i} done")
    if (i==500):
        break

keyword_dict_json = json.dumps(keyword_dict, indent=2)
print("Done")

with open("forward.json","w") as myFile:
    myFile.write(keyword_dict_json)
    
