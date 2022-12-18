import json

data = json.load(open("tempX.json"))

for word in data:
    print(word)
    for doc in data[word]:
        print(doc[0][1])
    print("--------------------------------------------------")
    # break