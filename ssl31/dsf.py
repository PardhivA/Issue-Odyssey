import json
with open("issues_commit_summarization.json",'r') as f:
    data = json.load(f)
    data = list(data)
    print(data[0]['issue_index'])