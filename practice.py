import nltk
import json
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from pathlib import Path

root = Path('dataset')

file_objs = root.iterdir()
files = []
for i in file_objs:
    files.append(str(i))

# .split('/')[1]

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


# # open file
# file = open('bbc.json')
# json_data = json.load(file)


# keyword_list = []
# keyword_dict = {}

for file in files:
    filename = file.split('/')[1]
    file = open(file)
    json_data = json.load(file)

    keyword_list = []
    keyword_dict = {}

    for i in range(len(json_data)):
        doc_list_title = tokenize(json_data[i]['title'])
        doc_list_content = tokenize(json_data[i]['content'])

        for j in range(len(doc_list_title)):
            if(doc_list_title[j] not in keyword_dict and doc_list_title[j] not in stop_words):

                #append the new word to the keyword list
                keyword_list.append(doc_list_title[j])

                #create a new entry in the dictionary
                keyword_dict[doc_list_title[j]] = []

                #append the document number and the position of the keyword in the document in a list
                #separately
                keyword_dict[doc_list_title[j]].append([[filename,i,1],[j]])

            elif(doc_list_title[j] in keyword_dict): #if the word is already in the dictionary
                flag = False
                for k in range(len(keyword_dict[doc_list_title[j]])):

                    if(keyword_dict[doc_list_title[j]][k][0][1] == i):
                        keyword_dict[doc_list_title[j]][k][0][2] += 1
                        keyword_dict[doc_list_title[j]][k][1].append(j)
                        flag = True
                        break
                if flag == False:
                    keyword_dict[doc_list_title[j]].append([[filename,i,1],[j]])

        for j in range(len(doc_list_content)):
            if(doc_list_content[j] not in keyword_dict and doc_list_content[j] not in stop_words):

                #append the new word to the keyword list
                keyword_list.append(doc_list_content[j])

                #create a new entry in the dictionary
                keyword_dict[doc_list_content[j]] = []

                #append the document number and the position of the keyword in the document in a list
                #separately
                keyword_dict[doc_list_content[j]].append([[filename,i,1],[j]])

            elif(doc_list_content[j] in keyword_dict): #if the word is already in the dictionary
                flag = False
                for k in range(len(keyword_dict[doc_list_content[j]])):

                    if(keyword_dict[doc_list_content[j]][k][0][1] == i):
                        keyword_dict[doc_list_content[j]][k][0][2] += 0.5
                        keyword_dict[doc_list_content[j]][k][1].append(j)
                        flag = True
                        break
                if flag == False:
                    keyword_dict[doc_list_content[j]].append([[filename,i,1],[j]])
        
        if(i%500 == 0):
            print(i, " documents processed")
        



keyword_dict_json = json.dumps(keyword_dict, indent=1)
print("Done")

with open("reverseFin.json","w") as myFile:
    myFile.write(keyword_dict_json)
    
