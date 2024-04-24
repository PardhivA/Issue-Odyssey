
                
import json
import os
# with open("SWELinker30/issues_commit_summarization_individual.json",'r') as f:

#     data = json.load(f)
#     data = list(data)
    
a = None
with open("/home/ssl31/Downloads/SWELinker30/AnIssueData.json") as f:
    a = json.load(f)
b = a.copy()
for issue in b:
    k = ""
    for commit in issue["CommitDetails"]:
        k += commit["method_summarization"]
    issue["Total summary"] = k
    del issue["CommitDetails"]
    
print("did something here")
with open("./AnIssueSummarization.json","w") as out:
    json.dump(b,out)