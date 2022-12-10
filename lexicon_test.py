from pathlib import Path
import json
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords


# return to monkey
def stopWords_remmover_and_lemmatizer(pos_tags):
    lemmatizer = WordNetLemmatizer()
    required = ['n','v','r','a']
    keywords = []
    for i in pos_tags:
        if (i[1][0].lower() in required):
            keywords.append(lemmatizer.lemmatize(i[0],i[1][0].lower()))
    return keywords


# as the name suggests tokenizes a sentence or entire paragraph
def tokenize(sentence):
    tokens = nltk.word_tokenize(sentence.lower())

    clean_tokens = [word for word in tokens if word not in stop_words]

    pos_tags = nltk.pos_tag(clean_tokens)
    keywords = stopWords_remmover_and_lemmatizer(pos_tags)
    return keywords

stop_words = stopwords.words('english')
stop_words.append('@')
stop_words.append('.')
stop_words.append(',')
stop_words.append('\u2014')



# define the path to the dataset
root_dir = Path("/home/java/dataset/dataverse_files/json/nela-gt-2021/newsdata")

# make it iterable
file_paths = root_dir.iterdir()

all_words = []
# iterate over all files
for item in file_paths:
    # turn the posix type to a string to be used by open function
    current_file_path = str(item)
    file = open(current_file_path)

    json_data = json.load(file)
    
    for i in range(len(json_data)):
        doc_list = tokenize((json_data[i]['title'])+" "+(json_data[i]['content']))

        for j in doc_list:
            if(j not in all_words):
                all_words.append(j)
            else:
                pass
        print(f"Article {i} done")
    print(f"File {item} done")
    

all_words_set = set(all_words)

lexicons = json.dumps(all_words_set, indent=4)     


with open('lexicon.json','w') as outFile:
    outFile.write(lexicons)
    outFile.close()

print("[DONE]")
    