from datetime import datetime
import requests
import json

import requests
from pydriller import Repository
import os
import signal
import time

from transformers import AutoModelForCausalLM, AutoTokenizer

device = "cpu" # the device to load the model onto

model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")
tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")
import re
# from issue_commit_v2 import  extract_number
def extract_number(text):
 """
 Extracts a number followed by "%" from a string using regular expressions.

 Args:
     text: The string to search for a number followed by "%".

 Returns:
     The extracted number as a string, or None if no number is found.
 """

 # Use regular expression to find digits followed by "%"
 match = re.search(r"\d+%", text)
 if match:
   return match.group()[:-1]  # Return digits only (excluding "%")
 else:
   return None

import json


def find_issue_match_percent(issue_commits_arr, i, j):
    # issue_title = ""
    # if issue["title"] != None:
    #    issue_title  = issue["title"]
    # issue_body = ""
    # if issue["body"] != None:
    #    issue_body  = issue["body"]
    #  **************** TAKING ONLY THE TITLE AND BODY OF ISSUES FOR COMPARISON  ********
    issue1 = {"issue_title": issue_commits_arr[i]["title"], "issue_body": issue_commits_arr[i]["body"]}
    issue2 = {"issue_title": issue_commits_arr[j]["title"], "issue_body": issue_commits_arr[j]["body"]}
    temp1 = " Here is the info of issue 1: " + json.dumps(issue1)
    temp2 = " Here is the info of issue 2: " + json.dumps(issue2)
    askMistral = temp1 + temp2
    print("askingMistrak",i, j)
    # print(temp)
    messages=[{
                    'role': 'user',
                    'content': '''You are given two issues. Each issue consists of the issue title, issue body. Now, compare those two issues and give me a percentage of similarity between the issues if they are talking about the same thing. Give 30% weightage to similarity in issue_titles, and rest of the weightage to similarity in issue_bodies.  Do not output any explanation . Here are some examples:
                    INPUT:
						 Here is the info of issue 1:  
        "issue_title": "[Bug] [r2258] Mix up of chapters in the reader with vertical paging.", "issue_body": "**Describe the bug**\r\nVertical paging.\r\n\r\nhttps://user-images.githubusercontent.com/75091899/171745391-9458cd6a-e1fc-495b-b68b-a0b7870542ae.mp4\r\n\r\n\r\n**To Reproduce**\r\nSteps to reproduce the behavior:\r\n1. Open a chapter with vertical paging on\r\n2. Keep clicking in the middle of the screen like in the video\r\n\r\n**Expected behavior**\r\nThe reader shouldn't mix up chapters with part of previous chapters.\r\n\r\n**Screenshots**\r\nIf applicable, add screenshots to help explain your problem.\r\n\r\n**Device information:**\r\n - OS: Android 8\r\n - App Version: r2258\r\n\r\n**Additional context**\r\nAdd any other context about the problem here.\r\n"
        
        Here is the info of issue 2: 
         "issue_title": "[Bug] [r2089] Reader strange scrolling bug between chapters", "issue_body": "**Describe the bug**\r\nVertical mode\r\n\r\n\r\nhttps://user-images.githubusercontent.com/75091899/166258783-14169752-6035-44ef-a54e-650dfd5eaa12.mp4\r\n\r\ni think this video is sufficent.\r\n\r\n**To Reproduce**\r\nSteps to reproduce the behavior:\r\n1. Vertical mode on\r\n2. Show divider OFF\r\n3. see video\r\n\r\n**Expected behavior**\r\nthe scrolling between chapters should be fluud\r\n\r\n\r\n**Device information:**\r\n - OS: android 8\r\n - App Version: r2089\r\n\r\n**Additional context**\r\nAdd any other context about the problem here.\r\n", 
                        
                    OUTPUT: 100%.

                        Another example:
                        INPUT:
                     Here is the info of issue 1: 
        "issue_title": "[Bug] [2.0.0-2344] Migrate source button malfunctioning",
        "issue_body": "**Describe the bug**\r\nThe menu button to migrate a novel's source to a another source seems to be broken.\r\n\r\n**To Reproduce**\r\nSteps to reproduce the behavior:\r\n1. Open Shosetsu\r\n2. Install at least two extensions\r\n3.  Add a novel (a novel within both shouldn't be necessary)\r\n4. Enter the added novel's chapter list view\r\n5. Click or tap the overflow menu within the novel chapter list view\r\n6. Click or tap the \"Migrate source\" overflow menu option\r\n7. Experience the suck. Then embrace the suck. A worldview needed for almost everything in life for those who experience sucky situations or events.\r\n\r\n**Expected behavior**\r\nThe expected behavior is for the user to be able to migrate sources for a novel without experiencing setbacks.\r\n\r\n**Screenshots**\r\nI'm getting tired from typing extra details... it should be fine.... maybe?\r\n\r\n**Device information:**\r\n - OS: Android 10 \r\n - App Version: 2.0.0-2344\r\n\r\n**Additional context**\r\nAdditional context: As my grandpappy always said, \"What a load of bullshit!\"\r\n",
        
        
        Here is the info of issue 2: "issue_index": 230,
        "issue_title": "[F-R] Change export backup dialog to be easily understood",
        "issue_body": "**Is your feature request related to a problem? Please describe.**\r\nThe export dialog currently seems to not fit the function it enacts. \r\n\r\n**Describe the solution you'd like**\r\nChange the export dialog from \"Export location\" to something along the lines of \"Select backup\"\r\nor \"Select backup to export\"\r\n\r\n**Describe alternatives you've considered**\r\nI believe there isn't a sufficient alternative to this enhancement suggestion.\r\n\r\n**Additional context**\r\nI believe this enhancement report is sufficiently explained.\r\n",
        
                    OUTPUT: 10%.
                    
                    
                    The similarity in the mapping of the issue and issue must be given as a percentage only. Do not use any common language words to describe their similarity. We need asnwer only in percentages.

    	 
                       ''',
                },{
                    'role': 'assistant',
                    'content': 'ok, OUTPUT will be given only in percentage and no other text/explanation will be provided',
                },
                {
                    'role': 'user',
                    'content':  askMistral,
				}

                ]

    encodeds = tokenizer.apply_chat_template(messages, return_tensors="pt")
    model_inputs = encodeds.to(device)
    model.to(device)
    generated_ids = model.generate(model_inputs, max_new_tokens=1000, do_sample=True)
    decoded = tokenizer.batch_decode(generated_ids)
    response = decoded[0]

    
    temp = response.split("[/INST]")
    # print(temp[1])
    print("yes ia m here")
    req = temp[len(temp)- 1]
    answer = extract_number(temp[len(temp)- 1])
    if answer == None:
     if req.find('low') != -1:
         answer = '0'
     elif req.find('high') != -1:
         answer = '40'
     else:
         answer  ='0'
    # print("\n\n\n\n\n numerical number" + answer + "\n\n\n\n\n")
    return int(answer)

from dsu import DSU

def issue_issue_map_fun(issue_commits_arr):
    # issue_commits_arr : has issues title, body, and all matching commits summarizations
    n = len(issue_commits_arr)
    mp = {}
    union_find = DSU(n)
    for i in range(n):
        mp[issue_commits_arr[i]['Id']] = i
    
    with open("map_of_issue_to_number_ilinker.json",'w') as wrwr:
        json.dump(mp, wrwr)
    
    issue_and_related_issue = {}
    for i in range(n):
        if i < 99:
           continue
        print("current i", i)
        current_issue_number = mp[issue_commits_arr[i]['Id']]
        if(str(current_issue_number) not in issue_and_related_issue):
            issue_and_related_issue[current_issue_number] = {"issueNumber": current_issue_number, "similarity_percentage": str(100)}
        for j in range(i+1, min(i+100,n)):
            print("cuyrrent j", j)
            percent = find_issue_match_percent(issue_commits_arr, i, j)
            issue_num_i = issue_commits_arr[i]['Id']
            issue_num_j = issue_commits_arr[j]['Id']
            x = mp[issue_num_i]
            y = mp[issue_num_j]
            print(x,"==",issue_num_i,"   ", issue_num_j,"==" ,y, "  ===>  ",percent)
            if percent > 40:
                union_find.union(x,y)
                issue_and_related_issue[y] = {"issueNumber": union_find.find(y), "similarity_percentage": str(percent)}
                issue_and_related_issue[x] = {"issueNumber": union_find.find(x), "similarity_percentage": str(percent)}
                with open("relation_issue_issue_ilinker.json",'w') as iir:
                    json.dump(issue_and_related_issue, iir)
                
    return union_find, mp



with open('moment_issues.json', 'r') as file:
    issues= json.load(file)

b = issues.copy()
# for issue in b:
#     k = ""
#     for commit in issue["CommitDetails"]:
#         k += commit["method_summarization"]
#     issue["Commit summary"] = k
#     del issue["CommitDetails"]
    
print("did something here")
with open("./test1.json","w") as out:
    json.dump(b,out)

    
ds, mp = issue_issue_map_fun(issues)