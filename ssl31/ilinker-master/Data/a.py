import pandas 
import json
import csv
import os

def  lll(ifile,ofile):
    data =[]
    with open(ifile, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        data = [row for row in reader] 


    with open(ofile, 'w') as jsonfile:
        json.dump(data, jsonfile)


lll("./moment_issues.csv","./moment_issues.json")