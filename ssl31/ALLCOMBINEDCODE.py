######################################################

#ALL GITHUB REPO AND JSON HELPER FUNCTIONS ARE HEREE!!!!!!!!!!!
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
    _, __, ___, identifier = match.groups()
    return identifier
  else:
    return None

def only_get_reponame(url):
  pattern = r"https://github.com/([^/]+)/([^/]+)/(.+)/(\d+)"
  match = re.match(pattern, url)
  if match:
    _, reponame, ___, __ = match.groups()
    return reponame
  else:
    return None

import json
import os

def create_repo_folder(reponame):
    # Create the folder if it doesn't exist
    os.makedirs(reponame, exist_ok=True)

def load_from_json(reponame, filename):
    #create folder if it doesn't exist
    create_repo_folder(reponame)

    # Path to the JSON file
    file_path = os.path.join(reponame, filename)

    data = None

    # Return data from the JSON file
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)

    return data

def write_to_json(data, reponame, filename):
    #create folder if it doesn't exist
    create_repo_folder(reponame)

    # Path to the JSON file
    file_path = os.path.join(reponame, filename)

    # Write the data to the JSON file
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file)

def append_to_json(data,reponame, filename):
    # Read existing data from JSON file
    create_repo_folder(reponame)

    file_path = os.path.join(reponame, filename)

    existing_data = {}
    if os.path.exists(file_path):
        with open(file_path, 'r') as json_file:
            existing_data = json.load(json_file)

    # Update existing data with new data
    existing_data = list(existing_data)
    existing_data.append(data)

    # Write updated data back to JSON file
    with open(file_path, 'w') as json_file:
        json.dump(existing_data, json_file, indent=4) 

def check_json_file_exists(file_path):
    return os.path.isfile(file_path) and file_path.lower().endswith('.json')

######################################################














###################################################

# ISSUE COMMIT MATHCIGN CODE 
# ALL ISSUE COMMIT MATCHING CODE WILL BE IN THE ISSUE COMMIT MATCHING FUNCTION 

######################################################

def issue_commit_matching_function(html_url_of_github_issue):
  import requests
  from pydriller import Repository
  import os


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

  githubinfo_of_current_issue = extract_github_info(html_url_of_github_issue)
  username_of_repo = githubinfo_of_current_issue["username"]
  reponame_of_repo  = githubinfo_of_current_issue["repositoryName"]

  # GitHubHandler = GithubFetcher("shosetsuorg","shosetsu", ["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"])
  # issues = GitHubHandler.get_issues({"state":"closed", "per_page":"100"})
  GitHubHandler = GithubFetcher(username_of_repo,reponame_of_repo, ["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"])
  issues = GitHubHandler.get_issues({"state":"closed", "per_page":"100"})


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
    issue_managed_at[2] = issue_managed_at[2].split('T')
    return [int(issue_managed_at[0]), int(issue_managed_at[1]), int(issue_managed_at[2][0])]


  from transformers import AutoModelForCausalLM, AutoTokenizer

  device = "cpu" # the device to load the model onto

  model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")
  tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")



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


  issue_commit_map = []
  j = 0
  for issue in issues:
      ## checking...
      
      j = j + 1
      print('\n\n\n\n')
      print("issue_count: ", j)
      print('\n\n\n\n')

      issue_created_at = issue_date_generator(issue, "created_at")
      issue_closed_at = issue_date_generator(issue, "closed_at")
      dt1 = datetime(issue_created_at[0], issue_created_at[1], issue_created_at[2], 0, 0, 0)
      dt2 = datetime(issue_closed_at[0], issue_closed_at[1], issue_closed_at[2], 23, 59, 0)

      Commits = pydriller.Repository('../Downloads/shostesu/shosetsu', since=dt1, to=dt2).traverse_commits()
      i = 0
      num = 0
      CommitDetails = []
      print(Commits)
      
      
      for commit in Commits:

          print(commit.msg)
          modified_files = []



          num = 0
          method_info = ""
          

          
          for m in commit.modified_files:
              modified_files.append(m)
          method_changes = []


          
          print(modified_files)
          for file in modified_files:
              if len(file.changed_methods) == 0:
                  continue
              

              
              num = num + 1
              print("num: ",num)
              iter3 = 0

              
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

          similarity_percentage = issue_commit_map_fun(issue, method_info)
          if(similarity_percentage >= 40):
              CommitDetails.append({ "index": i, "url" : "", "method_summarization": method_info})
         
      issue_commit = {"issue_index" : j,"issue_title" : issue["title"], "issue_body" : issue["body"], "issue_html_link": issue["html_url"], "issue_url": issue["url"],"CommitDetails" : CommitDetails } 
      json_string = json.dumps(issue_commit)
      json_string = json_string+'\n'

      append_to_json(json_string, reponame_of_repo, "issues_commit_summarization_individual.json")
      # file_path = reponame_of_repo+"/issues_commit_summarization_individual.json"
      # with open(file_path,'a') as f:
      #     f.write(json_string + '\n')       
      issue_commit_map.append({"issue_index" : j,"issue_title" : issue["title"], "issue_body" : issue["body"], "issue_html_link": issue["html_url"], "issue_url": issue["url"],"CommitDetails" : CommitDetails })

  # print(issue_commit_map)
  import json
  append_to_json(issue_commit_map, reponame_of_repo, "issues_commit_summarization.json")
  # file_path = reponame_of_repo+"/issues_commit_summarization.json"
  # with open("issues_commit_summarization.json",'a') as f:
  #     json.dump(issue_commit_map,f)

  issue_issue_matching_function(reponame_of_repo, username_of_repo)





















###################################################

# ISSUE ISSUE MATCHING CODE 
# ALL ISSUE ISSUE MATCHING CODE IS IN ISSUE ISSUE MATCHING FUCNTION

######################################################

def issue_issue_matching_function(reponame_of_repo, username_of_repo):
  from issue_commit_v1 import model, tokenizer, device, extract_number
  import json

  def find_issue_match_percent(issue_commits_arr, i, j):
      
      temp1 = " Here is the info of issue 1: " + json.dumps(issue_commits_arr[i])
      temp2 = " Here is the info of issue 2: " + json.dumps(issue_commits_arr[j])
      askMistral = temp1 + temp2

      messages=[{
                      'role': 'user',
                      'content': '''You are given two issues. Each issue consists of the issue title, issue body, and its commit details which contain method summarization which is nothing but commit summarization . Now, compare those two issues and give me a percentage of similarity between the issues if they are talking about the same thing. Give 30% weightage to similarity in issue_titles, 30% weightage to similarity in issue_bodies, and 40% weightage to similarity in commitsDetails while comparing the given two issues. If Commit Details are not there, then 50% to issue_title and 50% to issue_body. Do not output any explanation . Here are some examples:
                      INPUT:
              Here is the info of issue 1:  
          "issue_title": "[Bug] [r2258] Mix up of chapters in the reader with vertical paging.", "issue_body": "**Describe the bug**\r\nVertical paging.\r\n\r\nhttps://user-images.githubusercontent.com/75091899/171745391-9458cd6a-e1fc-495b-b68b-a0b7870542ae.mp4\r\n\r\n\r\n**To Reproduce**\r\nSteps to reproduce the behavior:\r\n1. Open a chapter with vertical paging on\r\n2. Keep clicking in the middle of the screen like in the video\r\n\r\n**Expected behavior**\r\nThe reader shouldn't mix up chapters with part of previous chapters.\r\n\r\n**Screenshots**\r\nIf applicable, add screenshots to help explain your problem.\r\n\r\n**Device information:**\r\n - OS: Android 8\r\n - App Version: r2258\r\n\r\n**Additional context**\r\nAdd any other context about the problem here.\r\n", "issue_html_link": "https://github.com/shosetsuorg/shosetsu/issues/220", "issue_url": "https://api.github.com/repos/shosetsuorg/shosetsu/issues/220", "Commit summary": " The changes added a new `mutableStateOf` variable `first` and wrapped the scrolling logic within an if condition to only scroll when the component has been rendered once (`first` is true). The change introduces a flag `first` to handle the scrolling to the maximum position only once when the state is fully loaded. I'm unable to provide a one-line summarization without seeing the specific lines of code for the before and after method changes. The changes made to the method resulted in removing the specific modifier for each component and replaced it with \"Modifier.fillMaxWidth()\" and \"Modifier.padding(bottom = 8.dp)\" for better readability and maintainability. The changes introduced a transformation using the `transformLatest` function and added a conditional statement to emit a value of 6 when the input is zero. After changes, the method now transforms and emits the value obtained from the repository based on a conditions (if value is not zero, emit the value, otherwise emit 3). The changes in the method appear to remove the error handling and notifications for specific exceptions (such as FilePermissionException, MissingFeatureException, EmptyResponseBodyException, IOException, HTTPException, and Exception). Instead, all exceptions now result in the same error notification and return a failure result. The method now returns an instance of `ReaderChapterEntity` directly, assigned to a variable named `chapter`. The changes made to the method simplified the if condition on Line 25 by introducing two new variables, `convert` and `chapterType`, which are assigned the values of `convertStringToHtml` and `extensionChapterTypeFlow.firstOrNull()`, respectively. The method now checks for both conditions with the aid of these variables in one single if statement.The method was changed from having no arguments and no return type to having a suspended function with `List<Int>` for chapterIds and `ReadingStatus` for readingStatus as arguments and no return type. It now overrides and makes an API call to update chapter reading status. The alteration changes the implementation of filtering and updating selected chapters' reading status, from using a local list and iterating through it to call an updateUseCase for each chapter, to a single call to the chapterRepo to update the reading status for all selected chapters. The method was modified to include an override suspension, a new parameter list, and a call to an `updateChapterBookmark` function using the ` chaptersDao` instance.The alteration changed the local processing of selected chapters to a remote call to update their bookmarks in the repository. The method now calls a repository function to update the bookmark status for multiple chapters in one call instead of individually filtering and updating each selected chapter.Before change: Method closed without implementing the suspension and override annotation. After change: Method is now an override suspending function that marks specified chapterIds as deleted using chaptersDao. The change added a `@Throws` annotation and suspendability to the method `insertDownloads` with the ability to handle `SQLiteException`. The method now deletes downloads from the database instead of the local data source.The change transforms the method to process a list of chapters instead of getting a single novel and adding a download for each chapter. The method now accepts a single `ChapterUI` argument, which is suspended and converted to a list before being invoked. It also accepts an array of `ChapterUI` and invokes each one in a suspended manner after converting them to a list. The method now accepts an Array or individual ChapterUI instance with suspending behavior, converts them, and invokes the method on the converted instances. (Before: invoked ChapterUIs directly in a non-suspended manner, after: performs the same function but with suspension and accepts an array)Before: Iterating through a list and calling a download method for each element. After: Calling the download method once with the entire list as an argument. (In other words: Changed from iterating through a list and calling download method for each chapter to calling the download method once for the entire list.) The change simplified the method call from iterating through the list and making an individual call for each item, to making a single call with the entire list as an argument. The change in the method removes the dependency on an external repository and the chapter type by passing the chapter object directly to the constructor instead. The changes removed the implementation for getting an extension and deleting a chapter passage, instead now just accepting a ChapterEntity object and passing it to the constructor. In simpler terms, the changes have simplified the method by removing the logic for getting an extension and deleting a chapter passage. The method now accepts an array instead of an object as an argument. The change does not significantly alter the method's functionality, as it merely switches from using `chapterUI` to `chapter` as the parameter name in the first line. The method still deletes a chapter entity by calling `deleteChapter` and `repo.delete`. The change does not alter the method's functionality, it only renames the parameter from 'chapterUI' to 'chapter'. The change simplified the code by removing the need to loop through each saved chapter and call deleteChapterPassageUseCase for each one, instead call the use case directly on the list of saved chapters. The change eliminates the need for converting the list to a typed array before passing it as an argument to the `downloadChapter` method. The change simplified the method by eliminating the need to iterate through each saved chapter individually, instead passing the entire list of saved chapters to the use case in one call. The change in this method involves modifying the argument passed to the \"downloadChapter\" function. Before the changes, it received a single element array, while after the changes, it now receives an array of elements. The method now filters and passes the selected and unsaved chapters for download in one line instead of iterating through the list. There were no changes made to this line of code. The line before and after the change are identical. Therefore, there is no one-line summarization of the alteration. The change removed unnecessary parentheses when calling the \"downloadChapter\" method. The change consolidates filtering and retrieving selected and saved chapters into a single line before deletion. The method now directly deletes the selected chapters instead of iterating through and deleting them one by one.The changes removed the try-catch block and the method call to get the chapter bookmarked flow from the first method, and eliminated the redundant method call to the data access object in each suspended method. In summary, the code was refactored to eliminate redundancy and improve readability.The changes resulted in removing the method body of the 'loadDownload' function and adding the @Throws annotation to both functions. The code change removed the error handling and rethrowing an exception, making the method now just returning a List<ExtLibEntity> without any exception handling. The changes removed the error handling and rethrowing of SQLiteException in the method.  The change removes the try-catch block around the dao.update() call. I cannot see the actual code you are referring to, so I cannot provide an accurate one-line summary of the alterations based on the given context. Please provide the code or a clear description of the changes for me to help you. The change removes the try-catch block around the method call to \"dao.delete(extensionEntity.toDB())\". Before, an exception was caught and re-thrown, now any exceptions are propagated up to the caller. The alteration removes the try-catch block around the method call to \"dao.insertAbort(extensionEntity.toDB())\", meaning that any SQLiteException will no longer be caught and re-thrown but instead propagated directly to the caller. After the changes, the method now downloads and decodes a JSON response from the given URL using the Gson library. Before the changes, it only downloaded the response and returned the body bytes, throwing exceptions in case of failure. The change converts the state variables into a StateFlow for better state handling. The changes added a new property \"selectedChaptersState\" to the method, which suggests the UI now tracks the selected chapters state. The response for toggling the bookmark was also modified to potentially include the number of chapters that can be deleted after toggling the bookmark. The changes filtered the received chapters based on their selection status before emitting them in the method.After changes, a SwipeRefresh component was added to the method for providing a refreshing functionality to the LazyColumn. The name of the class used in the method has been changed from \"MdcTheme\" to \"ShosetsuCompose\". The method's class name has been changed from \"MdcTheme\" to \"ShosetsuCompose\". The method's namespace or class name has been changed from \"MdcTheme\" to \"ShosetsuCompose\". The class name was changed from \"MdcTheme\" to \"ShosetsuCompose\". The method's enclosed class has been changed from \"MdcTheme\" to \"ShosetsuCompose\". The method's class type was changed from \"MdcTheme\" to \"ShosetsuCompose\". The method's class name has been changed from \"MdcTheme\" to \"ShosetsuCompose\". The method's name has been changed from \"MdcTheme\" to \"ShosetsuCompose\". The method's theme configuration was changed from \"MdcTheme\" to \"ShosetsuCompose\". The changes removed the \"Modifier.fillMaxWidth().padding(bottom = 8.dp)\" from each item, meaning that each item no longer has specific padding and width adjustments.The alteration removes redundant assignment of 'Modifier.fillMaxWidth().padding(bottom = 8.dp)' to a variable named 'modifier' in each line. Instead, the Modifier property is directly applied to the SliderSettingContent in the after changes. The modifications made to the code removed the extra padding and fillMaxWidth modifier from each SwitchSettingContent call. This means that each SwitchSettingContent item now only has the default padding below it and takes up only the necessary space. The changes in the method remove the specific padding of 8.dp for each setting item, instead, theModifier.fillMaxWidth() is applied for each item to fill the maximum width with no padding. Summary of alterations: The method's modification includes removing unnecessary modifier declarations and chaining them together for a cleaner code. Additionally, the use of the 'fillMaxWidth()' and 'fillMaxHeight(.4f)' modifier was changed to 'fillMaxWidth().fillMaxHeight(.4f)' for conciseness. No functional changes were made to the method.The method changes involved removing unnecessary whitespaces and adjusting the modifier chaining to improve code readability, but functionally the method remains the same. The changes seem to have removed redundant modifications to the modifier of some components, keeping only the essential modifications. The change introduces the usage of the `firstLatestValueFrom` operator to observe the `viewModel.openLastRead()` property, instead of just observing it. The method now sets \"user cancelled\" instead of \"invalid QR code\" when executing Line17. The changes made to the method resulted in the user cancellation being handled differently when scanning a QR code with an invalid format or missing permission. Instead of setting an invalid QR code, the method now sets user cancelled. The changes in the method have altered the condition for launching the QR code scanner, now only launching it when the viewModel's openQRScanner data is present. After the changes, the method now emits a signal to open the QR scanner when it is completed. It is impossible for me to provide a one-line summarization of method alterations without seeing the actual code and understanding the context of the changes. Before the change, the method tries to emit an event with a URL. After the change, the method first tries to emit a false event with openQRScanner and then tries to emit an event with a URL using data. The method change resulted in converting a method call into a method declaration"
          
          Here is the info of issue 2: 
          "issue_index": 1, "issue_title": "[Bug] [r2089] Reader strange scrolling bug between chapters", "issue_body": "**Describe the bug**\r\nVertical mode\r\n\r\n\r\nhttps://user-images.githubusercontent.com/75091899/166258783-14169752-6035-44ef-a54e-650dfd5eaa12.mp4\r\n\r\ni think this video is sufficent.\r\n\r\n**To Reproduce**\r\nSteps to reproduce the behavior:\r\n1. Vertical mode on\r\n2. Show divider OFF\r\n3. see video\r\n\r\n**Expected behavior**\r\nthe scrolling between chapters should be fluud\r\n\r\n\r\n**Device information:**\r\n - OS: android 8\r\n - App Version: r2089\r\n\r\n**Additional context**\r\nAdd any other context about the problem here.\r\n", "issue_html_link": "https://github.com/shosetsuorg/shosetsu/issues/198", "issue_url": "https://api.github.com/repos/shosetsuorg/shosetsu/issues/198", "Commit summary": "  The changes in the method result in rearranging the elements vertically with a consistent bottom padding and removing the padding from the item width. The BackupNow button now spans the full width of the container.The method title for the backup selection alert has been changed.The change in the method removes the line related to \"viewModel.volumeScrollingOption()\".The change adds a new property \"isBookmarked\" to each NovelCard in both COMPRESSED and COZY content, allowing the displayed cards to reflect the bookmark status of their corresponding items.I'm unable to see the specific code in your example, so I'll provide a general statement on how to create a one-line summarization of a method change:\n\nCompare the functionality of the method before and after the changes. Identify what the change does in terms of meaning and express it as concisely as possible in a single sentence.\n\nFor example, if before the changes, the method sorted an array of numbers, and after the changes, it now sorts an array of strings, you could summarize the change as: \"Changed method to sort an array of strings instead of numbers.\"\n\nAnother example, if before the changes the method multiply two numbers, and after the changes it multiplies an array of numbers, you could summarize the change as: \"Updated method to multiply multiple numbers using an array instead of just two numbers.\"\n\nPlease note that the exact summary will depend on the specific code you're analyzing.The code usage was changed from the androidx.compose.material library to the standard Tab.The method now assigns several properties to local variables before calling exit handler.The changes moved the variable assignments of `isTTSCapable`, `isTTSPlaying`, `isBookmarked`, and `isRotationLocked` before the `scaffoldState` assignment."

          
                          
                      OUTPUT: 100%.

                          Another example:
                          INPUT:
                      Here is the info of issue 1:  "issue_index": 232,
          "issue_title": "[Bug] [2.0.0-2344] Migrate source button malfunctioning",
          "issue_body": "**Describe the bug**\r\nThe menu button to migrate a novel's source to a another source seems to be broken.\r\n\r\n**To Reproduce**\r\nSteps to reproduce the behavior:\r\n1. Open Shosetsu\r\n2. Install at least two extensions\r\n3.  Add a novel (a novel within both shouldn't be necessary)\r\n4. Enter the added novel's chapter list view\r\n5. Click or tap the overflow menu within the novel chapter list view\r\n6. Click or tap the \"Migrate source\" overflow menu option\r\n7. Experience the suck. Then embrace the suck. A worldview needed for almost everything in life for those who experience sucky situations or events.\r\n\r\n**Expected behavior**\r\nThe expected behavior is for the user to be able to migrate sources for a novel without experiencing setbacks.\r\n\r\n**Screenshots**\r\nI'm getting tired from typing extra details... it should be fine.... maybe?\r\n\r\n**Device information:**\r\n - OS: Android 10 \r\n - App Version: 2.0.0-2344\r\n\r\n**Additional context**\r\nAdditional context: As my grandpappy always said, \"What a load of bullshit!\"\r\n",
          "issue_html_link": "https://github.com/shosetsuorg/shosetsu/issues/232",
          "issue_url": "https://api.github.com/repos/shosetsuorg/shosetsu/issues/232",
          "Commit Summary": ""
          
          Here is the info of issue 2: "issue_index": 230,
          "issue_title": "[F-R] Change export backup dialog to be easily understood",
          "issue_body": "**Is your feature request related to a problem? Please describe.**\r\nThe export dialog currently seems to not fit the function it enacts. \r\n\r\n**Describe the solution you'd like**\r\nChange the export dialog from \"Export location\" to something along the lines of \"Select backup\"\r\nor \"Select backup to export\"\r\n\r\n**Describe alternatives you've considered**\r\nI believe there isn't a sufficient alternative to this enhancement suggestion.\r\n\r\n**Additional context**\r\nI believe this enhancement report is sufficiently explained.\r\n",
          "issue_html_link": "https://github.com/shosetsuorg/shosetsu/issues/230",
          "issue_url": "https://api.github.com/repos/shosetsuorg/shosetsu/issues/230",
          "Commit Summary": ""
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
            answer = '60'
        else:
            answer  ='0'
      # print("\n\n\n\n\n numerical number" + answer + "\n\n\n\n\n")
      return int(answer)

  from dsu import DSU

  def issue_issue_map_fun(issue_commits_arr):
      # issue_commits_arr : has issues title, body, and all matching commits summarizations


      n = len(issue_commits_arr)
      mp = {}


      # union_find = DSU(n)


      for i in range(n):
          mp[issue_commits_arr[i]['issue_index']] = i

      
      write_to_json(mp, reponame_of_repo, "map_of_issue_to_number.json")
      
      # with open("map_of_issue_to_number.json",'w') as wrwr:
      #     json.dump(mp, wrwr)
      
      matrix = [[0 for _ in range(n+1)] for _ in range(n+1)]
      
      for i in range(min(100, n)):
          for j in range(i+1, min(100, n)):
              percent_match = find_issue_match_percent(issue_commits_arr, i, j)
              issue_num_i = issue_commits_arr[i]['issue_index']
              issue_num_j = issue_commits_arr[j]['issue_index']
              matrix[issue_num_i][issue_num_j] = percent_match
              matrix[issue_num_j][issue_num_i] = percent_match
              write_to_json(matrix, reponame_of_repo, "issue_issue_match_percent.json")
              # with open("issues_issue_match_percent.json", 'w') as f:
              #     json.dump(matrix, f)
                  
      # return union_find, mp



                  
  import json
  import os
      
  # a = None
  # with open("/home/ssl31/Downloads/SWELinker30/issues_commit_summarization_individual.json") as f:
  #     a = json.load(f)
  a = load_from_json(reponame_of_repo, "issues_commit_summarization_individual.json")

  b = a.copy()
  for issue in b:
      k = ""
      for commit in issue["CommitDetails"]:
          k += commit["method_summarization"]
      issue["Commit summary"] = k
      del issue["CommitDetails"]
      
  write_to_json(b, reponame_of_repo, "test1.json")
  # with open("./test1.json","w") as out:
  #     json.dump(b,out)


  # print(len(b), b[0])
      
  # ds, mp = issue_issue_map_fun(b)
  issue_issue_map_fun(b)
  # n = len(b)
  # print(mp)


  # for i in range(n):
  #     print("Element {}: Representative = {}".format(i, ds.find(i)))
          













#################

#####  #####  #
#   #  #   #  #
#####  #####  #
#   #  #      #
#   #  #      #

##################


from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
from gevent.pywsgi import WSGIServer
from dotenv import load_dotenv
import os
import requests



####APP LOADING####
app = Flask(__name__)
CORS(app)
############

def issue_issue_linker(data):


  # All the below code is fine, but for a second lets consdier that data we get from the frontend is not only hte issue number but the whole link of the github issue page

  #TEMPORARY CODE STARTS
  # https://github.com/([^/]+)/([^/]+)/(.+)/(\d+)

  #data is converted to html link below for the format we are going to use in issue_commit_matchign
    html_link = "https://github.com/"+data["username"]+"/"+data["repositoryName"]+"/issues/"+str(data["issueNumber"])

    reponame_of_the_issue = only_get_reponame(html_link)
    file_path = "/home/ssl31/Downloads/SWELinker30/"+reponame_of_the_issue+"issues_issue_match_percent.json"
    
    if(not check_json_file_exists(file_path)):
      #go and execute the above codes of creating the mapping of issue_commit
      #here data is the html url of the github issue
      issue_commit_matching_function(html_link)
      #I mean once issue and commit mapping is done then we again have to execite th ebelow code however

  #TEMPORARY CODE ENDS


    # issues = None
    # with open("/home/ssl31/Downloads/SWELinker30/test1.json") as f:
    #     issues = json.load(f)
    issues = load_from_json(reponame_of_the_issue, "test1.json")

    found_issue = None
    for issue in issues:
        cur_issue_data = extract_github_info(issue["issue_html_link"])

        if int(data["issueNumber"]) == int(cur_issue_data["issueNumber"]):
            found_issue = issue
            break
    
    # related_issues_matrix = None
    # with open("/home/ssl31/Downloads/SWELinker30/issue_issue_match_percent.json") as f:
    #     related_issues_matrix = json.load(f)
    related_issues_matrix = load_from_json(reponame_of_the_issue, "issue_issue_match_percent.json")
  
    related_issues_to_current_issue = related_issues_matrix[str(found_issue["issue_index"]-1)]

    all_possibly_related_issue_numbers = []
    for issue_number_2 in range(len(related_issues_to_current_issue)):
        if(related_issues_to_current_issue[issue_number_2]>60):
            all_possibly_related_issue_numbers.append(issue_number_2)
  

    the_related_issues_to_be_sent_to_front_end = []

    print(all_possibly_related_issue_numbers)
    
    for possibly_related_issue_number in all_possibly_related_issue_numbers:
        for issue in issues:
            if(issue["issue_index"]==int(possibly_related_issue_number)+1):
                the_related_issues_to_be_sent_to_front_end.append({"issue":issue, "similarity_percentage": related_issues_to_current_issue[possibly_related_issue_number]})

    return the_related_issues_to_be_sent_to_front_end



 
@app.route('/get_issues', methods=['GET', 'POST'])
def get_issues():
    if request.method == 'POST':
        # print("inside the api call")
        cur_issue_data = request.json
        # print(cur_issue_data)
        related_issues = issue_issue_linker(cur_issue_data)
        # print(related_issues)
        
        sendbacktoclient = []
        for related_issue in related_issues:
            issue_to_display = related_issue["issue"]
            similarity_per = related_issue["similarity_percentage"]
            object = {"issue_no": only_get_issue_number(issue_to_display["issue_html_link"]), "issue_link": issue_to_display["issue_html_link"], "issue_title": issue_to_display["issue_title"], "similarity_per":similarity_per}
            sendbacktoclient.append(object)
        
        return jsonify(sendbacktoclient)

    return None





if __name__ == '__main__':
    print("s")
    app.run('10.23.105.31', 5000, ssl_context='adhoc')
    print("h")







