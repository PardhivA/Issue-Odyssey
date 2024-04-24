a = None
import os
import json
with open("./issues_commit_summarization_individual.json") as f:
    a = json.load(f)
b = a.copy()
for issue in b:
    k = ""
    for commit in issue["CommitDetails"]:
        k += commit["method_summarization"]
    issue["Total summary"] = k
    del issue["CommitDetails"]

with open("./test1.json","w") as out:
    json.dump(b,out)


