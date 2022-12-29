import tkinter as tk
from tkinter import *
import json
import webbrowser


# Shameekh Code Start
file = json.load(open("RIndexJ.json"))

def callback(link):
    webbrowser.open_new(link)

def searchQuery(query, file):
    refactoredQuery = query.split(" ")

    if (len(refactoredQuery) == 1):
        if (query not in file):
            return []
        word = file[query]
        counter = 0
        result = []
        for i in word:
            result.append(i[0][0])
            print(i[0][0])
            counter += 1
        return result

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
    resultList = []
    for ele in resultantArticles:
        print(ele)
        resultList.append(ele)
        # counter += 1
    return resultList



# Shameekh Code End

def open_link(link):
  import webbrowser
  webbrowser.open(link)

window = tk.Tk()
window.geometry("450x450+0+0")
window.title("Kaavish")

frame = tk.Frame(window)
frame.grid()

label = tk.Label(frame, text="Enter your search query:", font=('lato', 30))
label.grid(row=0, column=0)

search_bar = tk.Entry(frame, width=50)
search_bar.grid(row=1, column=0)

def search():
    # Clear any previous results
    for widget in window.winfo_children():
        if widget != frame:
            widget.destroy()

    # Perform the search and display the results
    query = search_bar.get()
    results = searchQuery(query,file)

    print(1)

    counterSpecial = 1
    for i in results:
        # label = tk.Label(window, text=i, font=("Arial", 14))
        # label.grid(row=counterSpecial+4-1, column=0)
        # label.bind(f"<Button-{counterSpecial}>", lambda e:
        # callback(i))
        button = Button(window, text=i, command=lambda l=i: open_link(l))
        button.grid(row=counterSpecial+4-1, column=0)
        counterSpecial+=1

    # for i, result in enumerate(results):


search_button = tk.Button(frame, text="Search", command=search) #command empty here
search_button.grid(row=2, column=0)

addnewdoc_button = tk.Button(frame, text="Add a new document") #command='' here 
addnewdoc_button.grid(row=3, column=0, pady=10)

window.mainloop()