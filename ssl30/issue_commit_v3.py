import requests
from pydriller import Repository
import os
import signal
import time

class GithubFetcher:
    def __init__(self, owner, repo, api_keys):
        self.api_keys = api_keys
        self.current_key_index = 0
        self.rate_limit_wait_time = 60
        self.max_retries = 3
        self.retryable_exceptions = (
            requests.exceptions.RequestException,
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
            requests.exceptions.HTTPError,
        )
        self.reset_times = {}
        self.base_url = "https://api.github.com"
        self.owner = owner
        self.repo = repo
        self.issues = []
        self.commits = []

    def _key_handler(self):
        if len(self.api_keys) == 0:
            print("No API keys available")
            return None

        key = self.api_keys[self.current_key_index]
        self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
        return key

    def get_rate_limit_info(self, response):
        rate_limit_info = {
            "limit": int(response.headers["X-RateLimit-Limit"]),
            "remaining": int(response.headers["X-RateLimit-Remaining"]),
            "reset": int(response.headers["X-RateLimit-Reset"]),
        }
        return rate_limit_info

    def get(self, url, headers=None, params=None):
        if headers is None:
            headers = {}

        for attempt in range(1, self.max_retries + 1):
            try:
                headers["Authorization"] = f"token {self._key_handler()}"
                response = requests.get(url, headers=headers, params=params)
                response.raise_for_status()

                rate_limit_info = self.get_rate_limit_info(response)
                print(f"Rate limit info: {rate_limit_info},key used: {headers['Authorization']}")
                if rate_limit_info["remaining"] == 0:
                    print(
                        f"Rate limit reached. Waiting for {self.rate_limit_wait_time} seconds..."
                    )
                    time.sleep(self.rate_limit_wait_time)
                    continue

                if "GitHub-Authentication-Token-Expiration" in response.headers:
                    expiration_time = int(
                        response.headers["GitHub-Authentication-Token-Expiration"]
                    )
                    self.reset_times[
                        self.api_keys[
                            (self.current_key_index - 1 + len(self.api_keys))
                            % len(self.api_keys)
                        ]
                    ] = expiration_time
                    print(f"Key expires at {expiration_time}")

                current_key = self.api_keys[self.current_key_index - 1]
                if (
                    current_key in self.reset_times
                    and time.time() > self.reset_times[current_key]
                ):
                    del self.api_keys[self.current_key_index - 1]
                    del self.reset_times[current_key]
                    print(f"Key {current_key} expired. Removing.")
                    continue

                print("headers",headers)
                # json.dump(response.json(), open("data1.json", "w"))
                return response.json()

            except self.retryable_exceptions as e:
                if attempt == self.max_retries:
                    print(
                        f"Attempt {attempt}/{self.max_retries}: {e.__class__.__name__}"
                    )
                    if response:
                        print(f"Error details: {response.text}")
                    # raise
                else:
                    print(
                        f"Attempt {attempt}/{self.max_retries}: {e.__class__.__name__} occurred. Retrying..."
                    )

        return None

    def get_issues(self,params):
        url = f"{self.base_url}/repos/{self.owner}/{self.repo}/issues"
        headers = {"Authorization": f"token {self._key_handler()}"}
        response = requests.get(url, headers=headers,params = params)
        if response.status_code == 200:
            self.issues = response.json()
            self.save_issues(self.issues)
            return self.issues
        else:
            print(f"Failed to fetch issues: {response.status_code}")
            return []

    def get_commits(self, from_date=None, to_date=None):
        ret = []
        if from_date is None:
            self.commits = list(Repository(f"https://github.com/{self.owner}/{self.repo}").traverse_commits())
            ret = self.commits
            self.save_commits(self.commits)
        else:
            ret = list(Repository(f"https://github.com/{self.owner}/{self.repo}", since=from_date, to=to_date).traverse_commits())
        return ret

    def save_issues(self, issues):
        folder_path = f"{self.owner}/{self.repo}/issues"
        os.makedirs(folder_path, exist_ok=True)
        with open(f"{folder_path}/issues.txt", "w") as f:
            for issue in issues:
                f.write(f"Issue #{issue['number']}: {issue['title']}\n")

    def save_commits(self, commits):
        folder_path = f"{self.owner}/{self.repo}/commits"
        os.makedirs(folder_path, exist_ok=True)
        with open(f"{folder_path}/commits.txt", "w") as f:
            for commit in commits:
                f.write(f"Commit: {commit.hash} by {commit.author.name} - {commit.msg}\n")




from datetime import datetime
import requests
import json

GitHubHandler = GithubFetcher("shosetsuorg","shosetsu", ["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"])
## issues =
with open('moment_issues.json', 'r') as file:
    issues= json.load(file)

#with open("moment_issues.json",'r') as f:
# GitHubHandler.get_issues({"state":"closed", "per_page":"100"})
# print(issues)

import pydriller
from pydriller import *



def compare_strings(str1, str2):
  """
  Compares two strings of lines and returns a list of tuples containing information about changed lines in both strings.

  Args:
      str1: The first string to compare.
      str2: The second string to compare.

  Returns:
      A list of tuples containing information about changed lines in both strings.
  """
  # Split the strings into lists of lines
  lines1=""
  lines2=""

  if(str1!=None): lines1 = str1.splitlines()
  if(str2!=None): lines2 = str2.splitlines()

  # Find the longest list of lines
  max_len = max(len(lines1), len(lines2))

  # Initialize lists to store information about changed lines
  changed_lines_in_str1 = []
  changed_lines_in_str2 = []

  # Iterate through the lines
  for i in range(max_len):
    # Check if the lines are equal
    if i < len(lines1) and i < len(lines2) and lines1[i] == lines2[i]:
      continue
    # If lines are not equal, add info about changed lines in str1 and str2
    line_num = i + 1
    if i < len(lines1):
      line1_content = lines1[i]
    else:
      line1_content = ""
    if i < len(lines2):
      line2_content = lines2[i]
    else:
      line2_content = ""
    if line1_content != "":
      # changed_lines_in_str1.append(f"Line {line_num} in str1: {line1_content}")
      changed_lines_in_str1.append((line_num, line1_content))
    if line2_content != "":
      # changed_lines_in_str2.append(f"Line {line_num} in str2: {line2_content}")
      changed_lines_in_str2.append((line_num, line2_content))

  return changed_lines_in_str1, changed_lines_in_str2



def _getMethodBody(method, source_code, file):
    """
    Given a method, it returns the body of the method.
    :param method: the method
    :param source_code: the source code
    :param file: the file
    :return: the body of the method
    """
    if method and source_code:
        lines = source_code.split("\n")
        start = method.start_line
        end = method.end_line
        method_body = "\n".join(lines[start - 1 : end])
        return method_body
    return None

def issue_date_generator(issue, type):
  issue_managed_at = issue[type]
  issue_managed_at = issue_managed_at.split('-')
  issue_managed_at[2] = issue_managed_at[2].split(' ')
  return [int(issue_managed_at[0]), int(issue_managed_at[1]), int(issue_managed_at[2][0])]


from transformers import AutoModelForCausalLM, AutoTokenizer

device = "cpu" # the device to load the model onto

model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")
tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")

def find_last_occurrence(text, substring):

    # Method 1: Iterating through the string
    last_pos = -1
    for i in range(len(text)):
        if text[i:].startswith(substring):
            last_pos = i
    return last_pos


import re

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



def issue_commit_map_fun(issue, summarization):
    issue_title = ""
    if issue["title"] != None:
       issue_title  = issue["title"]
    issue_body = ""
    if issue["body"] != None:
       issue_body  = issue["body"]
    
    temp = " Here is the info: \n issue_title: " + issue_title +" \n issue_body: " + issue_body + " \nsummarization: "+ summarization
    print(temp)
    messages=[{
                    'role': 'user',
                    'content': '''Given an issue's details and a  commit's method change summarization, give me a percentage of similarity between the commit and the issue if they are talking about the same thing. Do not output any explanation . Here are some examples:
                    INPUT:
						issue_title: "[Bug] [2186]'Teleportation' to chapter when you click the resume button is wrong if the sort is the oppisite"
                        issue_body: "https://user-images.githubusercontent.com/75091899/170125379-289b87c2-a4be-4a93-bab1-67885cf3815c.mp4\r\n\r\nidk how to descrive it but here is the video\r\n\r\n**To Reproduce**\r\nSteps to reproduce the behavior:\r\n1. pick a novel with a lot of chapters\r\n2. mark as read 2/3 of the total amount\r\n3. reverse the sort direction of chapters\r\n4. click resume button\r\nyou will see for a second that tha app teleported to the wrong chapter (it should be the last read one 1004, but it teleporter at the end of the video to 473, visually)\r\n\r\n**Expected behavior**\r\nthe app teleported to the wrong chapter (visually) but it opened the right chapter so the bug is that the short animation where the app teleport to the actual chapter is wrong if the sort direction is the opposite from the default one\r\n\r\n**Screenshots**\r\nIf applicable, add screenshots to help explain your problem.\r\n\r\n**Device information:**\r\n - OS:  android 8\r\n - App Version: r2186\r\n\r\n**Additional context**\r\nAdd any other context about the problem here.\r\n"
                        commit_summarization: In the altered method, instead of using `indexOfFirst` to get the index of the first unread or unread chapter, the method uses `firstOrNull` to retrieve the first occurrence of an unread/unread chapter, and assigns the index of that chapter to the output variable.
                        
                    OUTPUT: 100%.

                        Another example:
                        INPUT:
                    issue_title: "Move app package to app.shosetsu.android"
                    issue_body: null
                    commit_summarization: "The change introduces the loading of extensions from a repository before restoring them, allowing for dynamic retrieval and modification of extensions"
                  
                    OUTPUT: 50%.
                    
                    Another example:
                    INPUT:
                    issue_title: "[Bug] [2.0.0-2344] Migrate source button malfunctioning"
                    issue_body: "**Describe the bug**\r\nThe menu button to migrate a novel's source to a another source seems to be broken.\r\n\r\n**To Reproduce**\r\nSteps to reproduce the behavior:\r\n1. Open Shosetsu\r\n2. Install at least two extensions\r\n3.  Add a novel (a novel within both shouldn't be necessary)\r\n4. Enter the added novel's chapter list view\r\n5. Click or tap the overflow menu within the novel chapter list view\r\n6. Click or tap the \"Migrate source\" overflow menu option\r\n7. Experience the suck. Then embrace the suck. A worldview needed for almost everything in life for those who experience sucky situations or events.\r\n\r\n**Expected behavior**\r\nThe expected behavior is for the user to be able to migrate sources for a novel without experiencing setbacks.\r\n\r\n**Screenshots**\r\nI'm getting tired from typing extra details... it should be fine.... maybe?\r\n\r\n**Device information:**\r\n - OS: Android 10 \r\n - App Version: 2.0.0-2344\r\n\r\n**Additional context**\r\nAdditional context: As my grandpappy always said, \"What a load of bullshit!\"\r\n"
                    commit_summarization: "The change introduces the loading of extensions from a repository before restoring them, allowing for dynamic retrieval and modification of extensions"
                  
                    OUTPUT: 0%.
                    
                    The similarity in the mapping of the issue and commit must be given as a percentage only. Do not use any common language words to describe their similarity. We need asnwer only in percentages.

    	 
                       ''',
                },{
                    'role': 'assistant',
                    'content': 'ok, OUTPUT will be given only in percentage and no other text/explanation will be provided',
                },
                {
                    'role': 'user',
                    'content':  temp,
				}

                ]

    encodeds = tokenizer.apply_chat_template(messages, return_tensors="pt")
    model_inputs = encodeds.to(device)
    model.to(device)
    generated_ids = model.generate(model_inputs, max_new_tokens=1000, do_sample=True)
    decoded = tokenizer.batch_decode(generated_ids)
    response = decoded[0]



    print("response: ", response)
    # temp = response.split("The percentage of mapping of issue and commit summarisation is ")
    temp = response.split("[/INST]")
    # print(temp[1])
    req = temp[len(temp)- 1]
    answer = extract_number(req)
    if answer == None:
     if req.find('low') != -1:
         answer = '0'
     elif req.find('high') != -1:
         answer = '60'
     else:
         answer  ='0' 
    print("\n\n\n\n\n numerical number" + answer + "\n\n\n\n\n")
    return int(answer)


class TimeoutException(Exception):
    pass
issue_commit_map = []
j = 0
for issue in issues:
    ## checking...
    if issue['state'] != 'closed':
        continue
    j = j + 1
    print('\n\n\n\n')
    print("issue_count: ", j)
    print('\n\n\n\n')
    # if len(issue_commit_map) > 1: break
    # if j<= 45: continue
    # print("j: ", j)
    # if j==2: break
    
    
    ## date generation
    
    # print(issue["created_at"])
    # print(issue["closed_at"])
    issue_created_at = issue_date_generator(issue, "created_at")
    issue_closed_at = issue_date_generator(issue, "closed_at")
    dt1 = datetime(issue_created_at[0], issue_created_at[1], issue_created_at[2], 0, 0, 0)
    dt2 = datetime(issue_closed_at[0], issue_closed_at[1], issue_closed_at[2], 23, 59, 0)
    # print(dt1,dt2)
    
    
    ## fetching commits
    
    Commits = pydriller.Repository('~/Downloads/Downloads/moment', since=dt1, to=dt2).traverse_commits()
    i = 0
    num = 0
    CommitDetails = []
    print(Commits)
    
    ## iterating over all commits
    
    max_time = 3*60  # Maximum execution time in minutes

    try:
        signal.alarm(max_time * 60)  # Convert minutes to seconds

        for commit in Commits:

            print(commit.msg)
            modified_files = []

            ## checking...
            
            # i = i + 1
            # if(i == 4): break
            num = 0
            method_info = ""
            
            ## get all modified files in that particular commit
            
            for m in commit.modified_files:
                modified_files.append(m)
            method_changes = []

            ## iterating over all  modified files
            
            print(modified_files)
            for file in modified_files:
                if len(file.changed_methods) == 0:
                    continue
                
                ## checking...
                
                num = num + 1
                print("num: ",num)
                iter3 = 0
                
                ## iterating over all modified methods in those modified files
                
                for method in file.changed_methods:
                    iter3 += 1
                    ## getting whole method before and after
                    method_before = next((x for x in file.methods_before if x == method), None)
                    print(method_before)
                    method_after = next((x for x in file.methods if x == method), None)
                    print(method_after)


                    ##  getting method body before and after
                    
                    body_before = _getMethodBody(method_before, file.source_code_before, file)
                    body_after = _getMethodBody(method_after, file.source_code, file)

                    changes_before = ""
                    changes_after = ""

                    ## getting only the changes of method body if they are changed only
                    
                    if body_before == None or body_after == None: pass
                    else: changes_before, changes_after =compare_strings(body_before, body_after)


                    ## getting changes before and after in a single string format
                    
                    _changes_before = ""
                    _changes_after = ""
                    for line_num, line_content in changes_before:
                        _changes_before = _changes_before + "Line" + str(line_num) + ": " + str(line_content) + "\n"
                    for line_num, line_content in changes_after:
                        _changes_after = _changes_after + "Line" + str(line_num) + ": " + str(line_content) + "\n"



                    print("changes_before: ", _changes_before)
                    print("changes_after: ", _changes_after)

                    method_changes.append([_changes_before, _changes_after])


                    ## getting summarization from gemini AI
                    
                    prompt = "before changes: " + _changes_before + "after changes: " + _changes_after
                    
                    # # response =  GeminiModel.prompt(prompt)
                    
                    messages=[{
                        'role': 'user',
                        'content': ''' You will receive two objects. One is the lines of code of a method before changes due to a commit and second one is also some lines of code of a method after changes, your job is to give me a one line summarization of the alteration (not interms of code but in terms of meaning) based on the before and after the method changes, only one line summarization
                        ''',
                    },{
                        'role': 'assistant',
                        'content': 'ok',
                    },
                    {
                        'role': 'user',
                        'content': prompt,
                    }
                    ]
                    ### we have to implement this here 




    # def my_function(data):
    #     # Simulate some processing time
    #     time.sleep(2)  # Replace with your actual function logic
    #     return data * 2
                    encodeds = tokenizer.apply_chat_template(messages, return_tensors="pt")

                    model_inputs = encodeds.to(device)
                    model.to(device)

                    generated_ids = model.generate(model_inputs, max_new_tokens=1000, do_sample=True)
                    
                    decoded = tokenizer.batch_decode(generated_ids)

                    print("summirization: ", decoded[0])
                    response = decoded[0]
                    temp = response.split("[/INST]")
                    response = temp[len(temp)- 1]
                    # print("summarization: ", response, "\n\n\n\n\n")
                    method_info = method_info + response


                    # break
                    # method_info = method_info + response
                    # print("iter: ", iter3)
                    # if iter3 == 2: break
                
                # print("num: ", num)
                # if num == 2: break
                # break
            similarity_percentage = issue_commit_map_fun(issue, method_info)
            if(similarity_percentage >= 40):
                CommitDetails.append({ "index": i, "url" : "", "method_summarization": method_info})
            # break
    except TimeoutException as e:
        print(f"Error is {e}")
    finally:
        signal.alarm(0)  # Reset timer (optional)

    issue_commit = {"issue_index" : j,"issue_title" : issue["title"], "issue_body" : issue["body"], "issue_id": issue["issue_id"], "CommitDetails" : CommitDetails } 
    json_string = json.dumps(issue_commit)
    with open("issues_commit_summarization_individual_ilinker_new.json",'a') as f:
        f.write(json_string + '\n')       
    issue_commit_map.append({"issue_index" : j,"issue_title" : issue["title"], "issue_body" : issue["body"], "issue_id": issue["issue_id"],"CommitDetails" : CommitDetails })

# print(issue_commit_map)
import json
with open("issues_commit_summarization_ilinker_new.json",'a') as f:
    json.dump(issue_commit_map,f)
