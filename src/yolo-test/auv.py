
# Created by Can Toraman (toraman@usc.edu)
# October 16th, 2020
# Written in Python3

# Written for University of Southern California's Autonomous Underwater Vehicle Branch
# Use case: move Labelbox data (CVS export) to YOLOv2/v3/v4 required format
# MIT License


from termcolor import colored
import os
import sys
import csv # to parse down csv
import json # to parse down csv
import requests # to get image from the web
import shutil # to save it locally and move to the desired directory


# # STEP 1 : VERIFY PARENT DIRECTORY
# print()
# print(colored("STEP 1. VERIFYING PARENT DIRECTORY", "green"))

# path = os.getcwd()
# print("The directory will be created in the directory " + colored(path, "yellow"))

# locationSatisfied = False
# terminate = False
# while locationSatisfied == False:
#     locationAccept = input("Do you accept('y/n') ")
#     if locationAccept == 'n':
#         print(colored("Please run this script inside your desired parent directory", "yellow"))
#         terminate = True
#         break
#     elif locationAccept == 'y':
#         locationSatisfied = True
#     else:
#         print()
#         print(colored("Please enter a valid input"), "yellow")


# if terminate:
#     print()
#     sys.exit(0)


# # STEP 2 : GET DATA DIRECTORY NAME - if you enter nothing the default name will be label-data
# print()
# print(colored("STEP 2. GETTING DATA DIRECTORY NAME", "green"))
# dirNameInput = input("What do you want the directory name to be (default name is label-data): ")
# dirNameInput = dirNameInput.strip()
# dirName = "label-data"

# change = False
# if (dirNameInput != ""):

#     dirNameAdjust = ""
#     counter = 0
#     for i in dirNameInput:
#         replace = i
#         if (i == " "):
#             if (counter == 0):
#                 replace = "_"
#             else:
#                 replace = "-"
#             change = True
#         dirNameAdjust += replace
#         counter += 1
    
#     if (change):
#         print()
#         print(colored("Your entered data had a space, and it was modified", "yellow"))
#         print("from " + colored(dirNameInput, "red") + " to " + colored(dirNameAdjust, "green"))
#         dirNameInput = dirNameAdjust
#     dirName = dirNameAdjust



# # STEP 3. CREATE DATA DIRECTORY
# print(colored("\nSTEP 3. CREATING DATA DIRECTORY", "green"))
# try:
#     os.mkdir(dirName)
# except OSError:
#     print (colored("Creation of the directory ", "red") + colored(dirName, "yellow") + colored(" failed.", "red"))
#     print (colored("The directory might already exist.", "red") + colored(" If so, enter a different name or change the existing directory name.", "yellow"))
#     sys.exit(0)
# else:
#     print (colored("Successfully created the directory " +  dirName, "green"))



# STEP 3. READ CSV - make sure your csv file name is data.csv
print(colored("\nSTEP 3. READING CSV - ", "green") + colored("make sure your csv filename is data.csv", "yellow"))

with open("data.csv") as csvfile:
    readCSV = csv.reader(csvfile, delimiter = ",")

    counter = 0
    for row in readCSV:
        url = row[2]
        labelLine = row[3]
        try:
            print(json.loads(labelLine))
        except ValueError as e:
            continue

        counter += 1
        filename = str(counter) +  ".jpg"
        
        r = requests.get(url, stream = True)
        if counter <= 500 and r.status_code == 200:
            # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
            r.raw.decode_content = True
            
            # Open a local file with wb ( write binary ) permission.
            with open(filename,'wb') as f:
                shutil.copyfileobj(r.raw, f)

                # moves the image under the /images directory
                shutil.move(os.getcwd() + "/" + filename, os.getcwd() + "/images")
                print('Image sucessfully Downloaded: ', filename)
            
            

