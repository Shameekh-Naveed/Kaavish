import tkinter as tk

window = tk.Tk()
window.geometry("450x450+0+0")
window.title("Kaavish")

frame = tk.Frame(window)
frame.pack(pady=50)

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
    results = perform_search(query)
    for i, result in enumerate(results):
        label = tk.Label(window, text=result, font=("Arial", 14))
        label.grid(row=i+4, column=0)


search_button = tk.Button(frame, text="Search", command=search) #command empty here
search_button.grid(row=2, column=0)

addnewdoc_button = tk.Button(frame, text="Add a new document") #command='' here 
addnewdoc_button.grid(row=3, column=0, pady=10)

window.mainloop()