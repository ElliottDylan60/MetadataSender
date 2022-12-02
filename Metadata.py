''' -- Imports -- '''
from tkinter import *
import tkinter as tk
import os
import socket
import xml.etree.ElementTree as ET

''' -- Global Variables -- '''
HOST = "IP_ADDRESS"
PORT = {PORT}
BUFFER_SIZE = 4096
FILENAME = "Send.xml"
FILESIZE = os.path.getsize(FILENAME)
selectedIndex = 0
SAVEDFILE = "Saved.txt"

''' -- Form Functions -- '''
# ListBox selected index changed
# User selected an item in the list box
def ListBox_Click(event):
    for i in ListBox.curselection():
        selectedIndex = i
# Send button pressed
def btnSend_Click():
    for i in ListBox.curselection():
        selectedIndex = i

    titleArtist = ListBox.get(selectedIndex)
    titleArtist = titleArtist.split('-')
    
    tree = ET.parse("Send.xml")
    root = tree.getroot()
    for title in root.findall("title"):
        title.text = titleArtist[0]
    for artist in root.findall("artist"):
        artist.text = titleArtist[1]
    tree.write("Send.xml")
    sendFile()
# Sends xml file to server
def sendFile():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    with open(FILENAME, "rb") as f:
        while True:
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                print("ERRROR")
                break
            print("FINISHED")
            s.sendto(bytes_read, (HOST, PORT))
            break
    s.close()
    
# Delete button pressed
def btnDelete_Click():
    selected_checkboxs = ListBox.curselection()
    for selected_checkbox in selected_checkboxs[::-1]:
        ListBox.delete(selected_checkbox)
        with open(SAVEDFILE, "r") as fileRead:
            lines = fileRead.readlines()
            pointer = 1
            with open(SAVEDFILE, "w") as fileWrite:
                for line in lines:
                    if pointer != selected_checkbox+1:
                        fileWrite.write(line)
                    pointer += 1
# Add button pressed
def btnAdd_Click():
    titleArtist = ""
    titleArtist += txtTitle.get("1.0", "end-1c")
    titleArtist += "-"
    titleArtist += txtArtist.get("1.0", "end-1c")
    ListBox.insert(0, titleArtist)
    name = ListBox.get(0)
    with open(SAVEDFILE, "a") as fileAppend:
        fileAppend.write(name + "\n")
    txtTitle.delete(1.0, END)
    txtTitle.insert(1.0, "")
    txtArtist.delete(1.0, END)
    txtArtist.insert(1.0, "")
    
def AddAllFromFile():
    file = open(SAVEDFILE, "r")
    for line in file:
        ListBox.insert(END, line)
''' -- Initialize Form -- '''
# Form
root = tk.Tk()
root.title("Meta Data")
root.geometry("500x430")
# List Box
ListBox = Listbox(root, width=50, height=25)
ListBox.pack(anchor=tk.W)
ListBox.bind("<<ListboxSelect>>", ListBox_Click)
# Send Button
btnSend = Button(root, width=7, height=0, text="Send", command=btnSend_Click)
btnSend.pack(anchor=tk.W)
# Delete Button
btnSend = Button(root, width=7, height=0, text="Delete", command=btnDelete_Click)
btnSend.place(x=245, y=404)
# Add Title Textbox
lbTitle = Label(root, text="Title")
lbTitle.place(x=305, y=5)
txtTitle = Text(root, width=15, height=0)
txtTitle.place(x=350, y=5)
# Add Artist Textbox
lbArtist = Label(root, text="Artist")
lbArtist.place(x=305, y=50)
txtArtist = Text(root, width=15, height=0)
txtArtist.place(x=350, y=50)
# Add Button
btnSend = Button(root, width=7, height=0, text="Add", command=btnAdd_Click)
btnSend.place(x=430, y=100)
AddAllFromFile();
# mainloop
root.mainloop()