import requests
from bs4 import BeautifulSoup
import os
from tkinter import *
from tkinter import filedialog
import mysql.connector
import webbrowser
import socket
import keyboard
import pyperclip
import time
import winsound


#os.chdir("C:/Users/Adrian/Desktop/Python/AutoUploader/")
global debug
debug = False

# TOOLS ----------------------------------------------------------------------
def Debug(message):
    global debug
    if (debug):
        print(message)

def GetOption():
    while True:
        event = keyboard.read_event(suppress=True)
        if event.event_type == keyboard.KEY_DOWN and event.name in ['1', '2', '3', '4']:
            return event.name
        
def GetFileOption():
    event = keyboard.read_event(suppress=True)
    if event.event_type == keyboard.KEY_DOWN and event.name in ['1', '2']:
        return event.name
# /TOOLS ----------------------------------------------------------------------

# MAIN ----------------------------------------------------------------------
def SelectFileWindow():
    filePath = filedialog.askopenfilename(title="Open video file!",
                                          filetypes= (("Video file","*.mp4"),))
    if not filePath:
        return False
    Debug("File path: " + filePath)
    return filePath

def CheckFileSize(filePath):
    try:
        fileSize = os.path.getsize(filePath)
        return fileSize  / (1024 * 1024)
    except FileNotFoundError:
        print("File not found.")
    except OSError:
        print("OS error occurred.")

def UploadVideo(filePath):
    # Check if file less than 200mb
    if (CheckFileSize(filePath) >= 200):
        return print("File must be less than 200MB!")
    else:
        # Start a session
        session = requests.Session()

        # Send a GET request to the website to retrieve the source code
        response = session.get("https://streamin.one/")

        # Parse site source, find id and key
        soup = BeautifulSoup(response.text, "html.parser")
        linkDiv = soup.findAll("a", attrs={"class":"copylink"})
        uploadLink = [link.get_text() for link in linkDiv]
        urlIdentifier = uploadLink[0].split("/")[-1]
        Debug("URL Identifier: " + urlIdentifier)

        keyDivs = soup.findAll("input", attrs={"id":"key"})
        uploadKey = [keyDiv['value'] for keyDiv in keyDivs]
        urlKey = uploadKey[0]
        Debug("URL Key: " + urlKey)

        # Send file with a POST request
        file = open(filePath,'rb')
        fileName = filePath.split("/")[-1]
        data = {'i': urlIdentifier, 'k': urlKey}
        files = {'f': (fileName, file, 'video/mp4', {'Expires': '0'})}
        postUrl = "https://streamin.one/post"
        upload_response = session.post(postUrl, files=files, data=data)

        # Show video location
        Debug("POST request status: " + str(upload_response.status_code))


        return "https://streamin.one/uploads/" + urlIdentifier + ".mp4"

def SelectFile():
    while True:
        os.system('cls')
        print("Select a video file to upload!")
        filePath = SelectFileWindow()
        if not filePath:
            print("You did not select a file, choose next action on your keyboard")
            print("1 - Try again")
            print("2 - Exit")
            while True:
                fileOption = GetFileOption()
                if (fileOption == "1"):
                    break
                elif (fileOption == "2"):
                    exit()
                else:
                    winsound.Beep(200, 500)
            continue
        else:
            print("File selected: " + filePath)
            return filePath

def PrintNextAction():
    print("Choose next action on your keyboard")
    print("1 - Copy link to clipboard")
    print("2 - Open link in browser")
    print("3 - Upload more videos")
    print("4 - Exit")

def ChooseNextAction(filePath, link):
    while True:
        option = GetOption()
        if (option == "1"):
            pyperclip.copy(link)
            print("Link copied!")
            time.sleep(2)
            os.system('cls')
            print("Select a video file to upload!")
            print("File selected: " + filePath)
            print("Uploading...")
            print("Video uploaded: " + link)
            PrintNextAction()
            continue
        elif (option == "2"):
            webbrowser.open(link)
            print("Opened in browser!")
            time.sleep(2)
            os.system('cls')
            print("Select a video file to upload!")
            print("File selected: " + filePath)
            print("Uploading...")
            print("Video uploaded: " + link)
            PrintNextAction()
        elif (option == "3"):
            filePath = None
            link = None
            break
        elif (option == "4"):
            exit()
        else:
            winsound.Beep(440, 500)


# /MAIN ----------------------------------------------------------------------

if __name__ == "__main__":
    while True:
        filePath = SelectFile()
        print("Uploading...")
        link = UploadVideo(filePath)
        print("Video uploaded: " + link)
        PrintNextAction()
        ChooseNextAction(filePath, link)

        
