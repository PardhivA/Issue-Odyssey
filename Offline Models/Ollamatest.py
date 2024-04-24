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



# Example usage:
# if __name__ == "__main__":
#     api_keys = ["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"]
#     owner = "lcompilers"
#     repo = "lpython"

#     fetcher = GithubFetcher(owner, repo, api_keys)
#     issues = fetcher.get_issues(None)
#     if issues:
#         print("Issues:")
#         for issue in issues:
#             print(f"Issue #{issue['number']}: {issue['title']}")

#     commits = fetcher.get_commits()


from datetime import datetime
import requests
import json

GitHubHandler = GithubFetcher("shosetsuorg","shosetsu", ["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"])
issues = GitHubHandler.get_issues({"state":"closed", "per_page":"100"})
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

# # Example usage
# str1 = """Line 1
# Line 2
# Same line
# Line 4"""

# str2 = """Line 1
# Changed line
# Same line
# New line"""

# lines_changed_in_str1, lines_changed_in_str2 = compare_strings(str1, str2)

# if lines_changed_in_str1:
#   print("Lines changed in str1:")
#   for line in lines_changed_in_str1:
#     print(line)

# if lines_changed_in_str2:
#   print("Lines changed in str2:")
#   for line in lines_changed_in_str2:
#     print(line)

# if not lines_changed_in_str1 and not lines_changed_in_str2:
#   print("No lines changed.")

# def compare_strings(string1, string2):
#     lines_string1=""
#     lines_string2=""
#     if(string1!=None): lines_string1 = string1.split('\n')
#     if(string2!=None): lines_string2 = string2.split('\n')

#     changes_before = []
#     changes_after = []

#     for line_num, (line1, line2) in enumerate(zip(lines_string1, lines_string2), start=1):
#         if line1.strip() != line2.strip():
#             changes_before.append((line_num, line1.strip()))
#             changes_after.append((line_num, line2.strip()))

#     print("COMAPRED STRINGS",changes_after)

#     return changes_before, changes_after

# if _name_ == "_main_":
#     string1 = """Your first long string here"""
#     string2 = """Your second long string here"""

#     changes_before, changes_after = compare_strings(string1, string2)

#     print("Lines before the change:")
#     for line_num, line_content in changes_before:
#         print(f"Line {line_num}: {line_content}")

#     print("\nLines after the change:")
#     for line_num, line_content in changes_after:
#         print(f"Line {line_num}: {line_content}")

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

import ollama

# response = ollama.chat(model='llama2', messages=[{
#    'role': 'user',
#    'content': ''' You will receive two objects. One is the lines of code of a method before changes due to a commit and second one is also some lines of code of a method after changes, your job is to give me a one line summarization of what is altered and the meaning of it based on the before and after the method changes, only one line summarization''',
#  },{
#    'role': 'user',
#    'content': ''' What is the value of a+b ?''',
#  }])
#print(response['message']['content'],'\n','\n','\n','\n','\n','\n','\n','\n','\n','\n','\n','\n','\n')

# from transformers import AutoModelForCausalLM, AutoTokenizer

# device = "cpu" # the device to load the model onto

# model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")
# tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")

issue_commit_map = []
j = 0
for issue in issues:
    # checking...
    # j = j + 1
    if len(issue_commit_map) > 1: break
    # if j <= 5: continue
    # print("j: ", j)
    # if j==2: break
    # date generation
    # print(issue["created_at"])
    # print(issue["closed_at"])
    issue_created_at = issue_date_generator(issue, "created_at")
    issue_closed_at = issue_date_generator(issue, "closed_at")
    dt1 = datetime(issue_created_at[0], issue_created_at[1], issue_created_at[2], 0, 0, 0)
    dt2 = datetime(issue_closed_at[0], issue_closed_at[1], issue_closed_at[2], 23, 59, 0)
    # print(dt1,dt2)
    # fetching commits
    Commits = pydriller.Repository('../Downloads/shostesu/shosetsu', since=dt1, to=dt2).traverse_commits()
    i = 0
    num = 0
    CommitDetails = []
    print(Commits)
    # iterating over all commits
    for commit in Commits:

        print(commit.msg)
        modified_files = []

        # checking...
        # i = i + 1
        # if(i == 4): break
        num = 0
        method_info = ""
        # get all modified files in that particular commit
        for m in commit.modified_files:
            modified_files.append(m)
        method_changes = []

        # iterating over all  modified files
        print(modified_files)
        for file in modified_files:
            if len(file.changed_methods) == 0:
                continue
            # checking...
            num = num + 1
            print("num: ",num)
            iter3 = 0
            # iterating over all modified methods in those modified files
            for method in file.changed_methods:
                iter3 += 1
                # getting whole method before and after
                method_before = next((x for x in file.methods_before if x == method), None)
                print(method_before)
                method_after = next((x for x in file.methods if x == method), None)
                print(method_after)


                #  getting method body before and after
                body_before = _getMethodBody(method_before, file.source_code_before, file)
                body_after = _getMethodBody(method_after, file.source_code, file)

                changes_before = ""
                changes_after = ""

                # getting only the changes of method body if they are changed only
                if body_before == None or body_after == None: pass
                else: changes_before, changes_after =compare_strings(body_before, body_after)


                # getting changes before and after in a single string format
                _changes_before = ""
                _changes_after = ""
                for line_num, line_content in changes_before:
                    _changes_before = _changes_before + "Line" + str(line_num) + ": " + str(line_content) + "\n"
                for line_num, line_content in changes_after:
                    _changes_after = _changes_after + "Line" + str(line_num) + ": " + str(line_content) + "\n"



                print("changes_before: ", _changes_before)
                print("changes_after: ", _changes_after)

                method_changes.append([_changes_before, _changes_after])


                # # getting summarization from gemini AI
                prompt = "before changes: " + _changes_before + "after changes: " + _changes_after
                # # # response =  GeminiModel.prompt(prompt)
                
                # messages=[{
                #     'role': 'user',
                #     'content': ''' You will receive two objects. One is the lines of code of a method before changes due to a commit and second one is also some lines of code of a method after changes, your job is to give me a one line summarization of what is altered and the meaning of it based on the before and after the method changes, only one line summarization
                #     ''',
                # },{
                #     'role': 'assistant',
                #     'content': 'ok',
                # },
                # {
                #      'role': 'user',
                #     'content': prompt,
                # }
                # ]
                # encodeds = tokenizer.apply_chat_template(messages, return_tensors="pt")

                # model_inputs = encodeds.to(device)
                # model.to(device)

                # generated_ids = model.generate(model_inputs, max_new_tokens=1000, do_sample=True)
                # decoded = tokenizer.batch_decode(generated_ids)
                # print("summirization: ", decoded[0])
                # response = decoded[0]
                # temp = response.split("[/INST]")
                # response = temp[len(temp)- 1]
                # print("summarization: ", temp[len(temp)- 1])
                # method_info = method_info + response


                # break
                

                response = ollama.chat(model='llama2', messages=[{
                    'role': 'user',
                    'content': ''' You will receive two objects. One is the lines of code of a method before changes due to a commit and second one is also some lines of code of a method after changes, your job is to give me a one line summarization of what is altered and the meaning of it based on the before and after the method changes, only one line summarization''',
                },{
                    'role': 'user',
                    'content': prompt,
                }])
                print("summarization: ", response['message']['content'])
                method_info = method_info + response['message']['content']


                method_info = method_info + response
                break
                # print("iter: ", iter3)
                # if iter3 == 2: break
            print("num: ", num)
            # if num == 2: break
            break
        CommitDetails.append({ "index": i, "url" : "", "method_summarization": method_info})
        break
    issue_commit_map.append({"issue_index" : j,"issue_title" : issue["title"], "issue_body" : issue["body"], "issue_html_link": issue["html_url"], "issue_url": issue["url"],"CommitDetails" : CommitDetails })

# print(issue_commit_map)
import json
with open("issues_commit_summarization.json",'w') as f:
    json.dump(issue_commit_map,f)