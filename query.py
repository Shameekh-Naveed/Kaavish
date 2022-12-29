import json
from pathlib import Path
# from builtins import set

file = json.load(open("RIndexJ.json"))

# root = Path("./bins")
# file_objs = root.iterdir()
# barrels = {}
# for i in file_objs:
#     barrels.update(str(i))

# for i in barrels.key():
#     file_objs2 = barrels[i].iterdir()
#     for j in file_objs2:
#         barrels[i].append(str(j))

# print(1)
        


def searchQuery(query, file):
    refactoredQuery = query.split(" ")

    if (len(refactoredQuery) == 1):
        if (query not in file):
            return
        word = file[query]
        counter = 0
        for i in word:
            print(i[0][0])
            counter += 1
        return

    listOfDics = []
    for term in refactoredQuery:
        termDic = {}
        for article in range(len(file[term])):
            termDic[file[term][article][0][0]] = file[term][article][0][1]
        listOfDics.append(termDic)

    resultantArticles = list(listOfDics[0].keys())

    for i in range(1, len(listOfDics)):
        tempList = []
        for j in range(len(resultantArticles)):
            if (resultantArticles[j] in listOfDics[i]):
                tempList.append(resultantArticles[j])
        resultantArticles = tempList

    counter = 0
    for ele in resultantArticles:
        print(ele)
        counter += 1


searchQuery("death theory", file)
