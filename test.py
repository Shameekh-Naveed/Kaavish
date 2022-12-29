# import re  # used to remove punctuation and special characters
# from nltk.corpus import stopwords
# import nltk
# import json
# import time
from pathlib import Path

# from nltk.stem import WordNetLemmatizer

# nltk.download("tagsets")
# nltk.download("stopwords")
# nltk.download("wordnet")
# nltk.download("averaged_perceptron_tagger")
# nltk.download("punkt")

# wordnet = WordNetLemmatizer()

# print(nltk.pos_tag(["President"]))


Path("bin").mkdir(parents=False, exist_ok=False)

with open("bin/stopwords.txt", "w") as f:
    f.write("This is a test file.")
    f.close()
