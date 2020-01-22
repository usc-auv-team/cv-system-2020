#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 19:14:44 2019

@author: conormccormack
"""

import pandas as pd
import numpy as np 
import os
import json
import requests
import urllib.request

# Import labels data to csv
def import_csv():
    df = pd.read_csv('export-2019-10-22T02_19_41.326Z.csv')
    
    # Drop all skipped labels
    df = df[df.Label != 'Skip']
    
    # Select useful labels
    df = df[['ID', 'Labeled Data', 'Label']]    
    return df


# Download images from url to pwd
def download_images(merged,r,pwd):
    # download imagei.jpg to working directory
    for i in range(r):
        url = (merged.iloc[i,1])
        req = requests.get(url)
        open("{pwd}/imgs/image{i}.jpg".format(i=i, pwd=pwd), 'wb').write(req.content)


# Read json file and convert data to yolov3 label format
# Generates and writes labels to txt files
def parse_labels_to_txt(pwd):
    # Load json data as nested py dicitonaries
    with open('labels.json') as json_file:
        data = json.load(json_file)
    
    # Dictionary of labels and associated class integer
    classID = {'Vampire Bouy': 0, 'Vampire Bouy ':0, 'Path Marker': 1, 'DraculaObject': 2, 'Draculaobject': 2, 'Vetalas': 3, 'Garlic': 4,'Draugar': 5, 'Bat': 6, 'Handle': 7, 'Coffin': 8, 'Crucifix': 9, 'Dracula': 10}
    
    # Initializing datafram of labels with ID, class, and coordinates
    cols = {'image_num':[], 'ID': [], 'class': [], 'x':[], 'y':[], 'width': [], 'height':[]}
    parsed_data = pd.DataFrame(cols)
    
    # Deleting all "Skip" labels from json
    size = len(data)
    to_delete = []
    for i in range(size):
        if (isinstance(data[i]['Label'], str)):
            # Prepend to to_delete if "Skip" label
            to_delete.insert(0,i)
    
    # Remove "Skip" labels from data object
    for i in range(len(to_delete)):
        del data[to_delete[i]]
    
    
    x_max = -1
    x_min = 9999999
    y_max = -1
    y_min = 9999999
    
    j = 0
    for i in data:
        # Append new label to dataframe for each label.
        for key in data[j]['Label']:
            geo_dict = data[j]['Label'][key][0]
            geo_list = geo_dict['geometry']
            # Top left is 0, top right is 1, bottom right is 2, bottom left is 3
            
            coordinates = []
            
            for corner in geo_list:
                coordinates.append([corner['x'], corner['y']])
            
            x_max = -1
            x_min = 9999999
            y_max = -1
            y_min = 9999999
            
            for k in range(len(coordinates)):
                if(coordinates[k][0] > x_max):
                    x_max = coordinates[k][0]  
                    
                if(coordinates[k][1] > y_max):
                    y_max = coordinates[k][1]  
                    
                if(coordinates[k][0] < x_min):
                    x_min = coordinates[k][0]
                
                if(coordinates[k][1] < y_min):
                    y_min = coordinates[k][1]
            
            # x and y coorindates are means of respective max's and min's
            x = (x_max + x_min)/2
            y = (y_max + y_min)/2
            # width, height are differences max's, min's
            width = x_max - x_min
            height = y_max - y_min
            parsed_data = parsed_data.append({'ID': data[j]['ID'], 'class': classID[key], 'x': x, 'y': y, 'width': width, 'height': height, 'image_num': j},ignore_index=True)
   

            file1 = open("{pwd}/txts/image{j}.txt".format(j=j, pwd=pwd), "w")
            file1.write("<{class_num}> <{x}> <{y}> <{width}> <{height}>".format(class_num = classID[key], x=x, y=y, width=width, height=height))
            file1.close()
            
        j = j + 1
    
    return parsed_data
   
# Creates img and txt directories for jpg and txt files    
def generate_export_directories(pwd):
    img_path = "{pwd}/imgs/".format(pwd=pwd)
    txt_path = "{pwd}/txts/".format(pwd=pwd)
    
    access_rights = 0o755
    
    if not os.path.exists(img_path):   
        try:
            os.mkdir(img_path, access_rights)
        except OSError:
            print("Creation of the directory {path} failed.".format(path=img_path))
        else:
            print("Succesfully created the directory {path} ".format(path=img_path))
    else:
        print("{path} already exists!".format(path=img_path))


    if not os.path.exists(txt_path):
        try:
            os.mkdir(txt_path, access_rights)
        except OSError:
            print("Creation of the directory {path} failed.".format(path=txt_path))
        else:
            print("Succesfully created the directory {path} ".format(path=txt_path))
    else:
        print("{path} already exists!".format(path=txt_path))


def main():
    pwd = os.getcwd()
    generate_export_directories(pwd)  
    # import label csv as pandas dataframe
    df = import_csv()
    # r = # of rows in dataframe, c = # of columns in dataframe
    r, c = df.shape
    parsed_labels = parse_labels_to_txt(pwd)
    merged = pd.merge(df, parsed_labels, how='inner', left_on='ID', right_on='ID')
    merged.to_csv("labels.csv", index = False)          
    #download_images(merged,r, pwd)    
    
    
if __name__== "__main__":
  main()

