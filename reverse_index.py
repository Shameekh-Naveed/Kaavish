import nltk
import json
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

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


keyword_list = []
keyword_dict = {}

for i in range(len(json_data)):
    doc_list = tokenize(json_data[i]['title']+" "+json_data[i]['content'])

    for j in range(len(doc_list)):
        if(doc_list[j] not in keyword_dict and doc_list[j] not in stop_words):

            #append the new word to the keyword list
            keyword_list.append(doc_list[j])

            #create a new entry in the dictionary
            keyword_dict[doc_list[j]] = []

            #append the document number and the position of the keyword in the document in a list
            #separately
            keyword_dict[doc_list[j]].append([[i],[j]])

        # format
        # "moscow" : [
        #   [[1],[2,3,4,5]],
        #   [[3],[1,2,3,4,5]]
        # ]


        elif(doc_list[j] in keyword_dict): #if the word is already in the dictionary
            flag = False
            for k in range(len(keyword_dict[doc_list[j]])):

                if(keyword_dict[doc_list[j]][k][0][0] == i):
                    keyword_dict[doc_list[j]][k][1].append(j)
                    flag = True
                    break
            if flag == False:
                keyword_dict[doc_list[j]].append([[i],[j]])

    print(f"Document {i} done")
    if (i==50):
        break

keyword_dict_json = json.dumps(keyword_dict, indent=1)
print("Done")

with open("reverse.json","w") as myFile:
    myFile.write(keyword_dict_json)
    
