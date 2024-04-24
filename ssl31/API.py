# from keras_preprocessing.sequence import pad_sequences

from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
from gevent.pywsgi import WSGIServer

# import google.generativeai as genai
from dotenv import load_dotenv
import os
import requests

# script_dir = os.path.dirname(os.path.abspath(_file_))
# model_path = os.path.join(script_dir, "model2.pth")

# from github import Github

#checking git push


###################################3
# safety_settings = [
#     {
#         "category": "HARM_CATEGORY_DANGEROUS",
#         "threshold": "BLOCK_NONE",
#     },
#     {
#         "category": "HARM_CATEGORY_HARASSMENT",
#         "threshold": "BLOCK_NONE",
#     },
#     {
#         "category": "HARM_CATEGORY_HATE_SPEECH",
#         "threshold": "BLOCK_NONE",
#     },
#     {
#         "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
#         "threshold": "BLOCK_NONE",
#     },
#     {
#         "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
#         "threshold": "BLOCK_NONE",
#     },
# ]
# genai.configure(api_key="AIzaSyDEWOQzsQZSILCax2fnrGbkmMKC2xBHOsE")
# model_gem = genai.GenerativeModel('gemini-pro')
############################

# import torch
# import numpy as np


####APP LOADING####
app = Flask(__name__)
CORS(app)
############




import re

def extract_github_info(url):
  pattern = r"https://github.com/([^/]+)/([^/]+)/(.+)/(\d+)"
  match = re.match(pattern, url)
  if match:
    username, repository_name, identifier_type, identifier = match.groups()
    return {"username": username, "repositoryName": repository_name, "issueorpull": identifier_type, "issueNumber":identifier}
  else:
    return None

def only_get_issue_number(url):
  pattern = r"https://github.com/([^/]+)/([^/]+)/(.+)/(\d+)"
  match = re.match(pattern, url)
  if match:
    username, repository_name, identifier_type, identifier = match.groups()
    return identifier
  else:
    return None

import json
def issue_issue_linker(data):
    issues = None
    with open("/home/ssl31/Downloads/SWELinker30/test1.json") as f:
        issues = json.load(f)
    found_issue = None
    for issue in issues:
        cur_issue_data = extract_github_info(issue["issue_html_link"])
        print("TESITNG HREE",data["issueNumber"], cur_issue_data["issueNumber"])
        if int(data["issueNumber"]) == int(cur_issue_data["issueNumber"]):
            found_issue = issue
            break
    
    # related_issues_matrix = None
    related_issues = None
    with open("/home/ssl31/Downloads/SWELinker30/relation_issue_issue.json") as f:
        related_issues = json.load(f)

    print(found_issue)
    print(related_issues)
    print(found_issue["issue_index"])
    # with open("/home/ssl31/Downloads/SWELinker30/issues_issue_match_percent.json") as f:
    #     related_issues_matrix = json.load(f)

    related_issue_number = str(found_issue["issue_index"]-1)
    # related_issues_to_current_issue = related_issues_matrix[str(found_issue["issue_index"]-1)]

    # all_possibly_related_issue_numbers = []
    # for issue_number_2 in range(len(related_issues_to_current_issue)):
    #     if(related_issues_to_current_issue[issue_number_2]>60):
    #         all_possibly_related_issue_numbers.append(issue_number_2)

    all_possibly_related_issue_numbers = []
    for temp in related_issues:
        issue_number, related_issue_number_of_this_issue = temp, related_issues[temp]["issueNumber"]
        if(int(related_issue_number_of_this_issue)==int(related_issue_number)):
            all_possibly_related_issue_numbers.append(issue_number)
    # for temp in related_issues:
    #     issue_number, related_issue_number_of_this_issue = temp, related_issues[temp]["issueNumber"]
    #     if(int(related_issue_number_of_this_issue)==int(related_issues[str(related_issue_number)]["issueNumber"])):
    #         all_possibly_related_issue_numbers[str(issue_number)] = str(related_issues[temp]["similarity_percentage"]) 

    the_related_issues_to_be_sent_to_front_end = []

    print(all_possibly_related_issue_numbers)
    
    # for possibly_related_issue_number in all_possibly_related_issue_numbers:
    #     for issue in issues:
    #         if(issue["issue_index"]==int(possibly_related_issue_number)+1):
    #             the_related_issues_to_be_sent_to_front_end.append({"issue":issue, "similarity_percentage": related_issues_to_current_issue[possibly_related_issue_number]})

    for possibly_related_issue_number in all_possibly_related_issue_numbers:
        for issue in issues:
            if(issue["issue_index"]==int(possibly_related_issue_number)+1):
                the_related_issues_to_be_sent_to_front_end.append({"issue":issue, "similarity_percentage": related_issues[possibly_related_issue_number]["similarity_percentage"]})

    return the_related_issues_to_be_sent_to_front_end




@app.route('/get_issues', methods=['GET', 'POST'])
def get_issues():
    if request.method == 'POST':
        print("inside the api call")
        cur_issue_data = request.json
        print(cur_issue_data)
        related_issues = issue_issue_linker(cur_issue_data)
        print(related_issues)
        
        sendbacktoclient = []
        for related_issue in related_issues:
            issue_to_display = related_issue["issue"]
            similarity_per = related_issue["similarity_percentage"]
            object = {"issue_no": only_get_issue_number(issue_to_display["issue_html_link"]), "issue_link": issue_to_display["issue_html_link"], "issue_title": issue_to_display["issue_title"], "similarity_per":similarity_per}
            sendbacktoclient.append(object)

        # # Make prediction
        # print("hi")
        # prediction = model_predict_dsh()
        # pred = prediction[1]
        # result = prediction[0]
        # pred_probability = "{:.3f}".format(np.amax(pred)) 
        
        return jsonify(sendbacktoclient)

    return None


# @app.route('/suggest', methods=['GET', 'POST'])
# def suggest():
#     # print("out")
#     if request.method == 'POST':
        
#         # Get suggestion
#         toxic_comment = request.json
#         if toxic_comment:
#             result = model_suggest_san(toxic_comment)
#             print("Suggetsions: ", result)
#             return jsonify(result=result)
       

#     return None

# @app.route('/repocheck', methods=['GET', 'POST'])
# def repocheck():
#     print("out")
#     if request.method == 'POST':
        
#         # Make prediction for all comments in the repository
        
#         url = request.json
#         repository = url.split("github.com/")[-1]  # Extract everything after "github.com/"
#         print(repository)
        
#         print(request.json)
#         prediction = model_repocheck(repository)
#         result = prediction
#         print("res: " , result)
#         return jsonify(result=result)

#     return None


if __name__ == '__main__':
    # m=model_predict_dsh("i don't need your opinion")
    # print(m[1][0][0])
    # k=model_repocheck("tensorflow/tensorflow")
    # print(k)
    print("s")
    app.run('10.23.105.31', 5000, ssl_context='adhoc')
    #http_server = WSGIServer(('10.23.105.31', 5000), app)
    print("h")
    #http_server.serve_forever()
