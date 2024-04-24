from issue_commit_v1 import model, tokenizer, device, extract_number
import json

def find_issue_match_percent(issue_commits_arr, i, j):
    # issue_title = ""
    # if issue["title"] != None:
    #    issue_title  = issue["title"]
    # issue_body = ""
    # if issue["body"] != None:
    #    issue_body  = issue["body"]
    
    temp1 = " Here is the info of issue 1: " + json.dumps(issue_commits_arr[i])
    temp2 = " Here is the info of issue 2: " + json.dumps(issue_commits_arr[j])
    askMistral = temp1 + temp2
    # print(temp)
    messages=[{
                    'role': 'user',
                    'content': '''You are given two issues. Each issue consists of the issue title, issue body, and its commit summarisation. Now, compare those two issues and give me a percentage of similarity between the issues if they are talking about the same thing. Give 25% weightage to similarity in issue_titles, 25% weightage to similarity in issue_bodies, and 50% weightage to similarity in commitsDetails while comparing the given two issues. Do not output any explanation . Here are some examples:
                    INPUT:
						 Here is the info of issue 1:  "issue_index": 235,
        "issue_title": "Multiple optimizations for performance",
        "issue_body": "- **[Add Immutable annotation to UI models](https://github.com/shosetsuorg/shosetsu/commit/86fd6559ea4d13d0b365b418255bb028fd773052)**. Its for describing that the model wont change to the compose compiler, making it generate more optimized code. For this I replaced all var variables with val to guarantee this.\r\n- **[Add UIUpdates UI model for pre-calculated time display](https://github.com/shosetsuorg/shosetsu/commit/9550f49d5cb9530c80441bb6bb02ed04854caf1f)** This allows for the time string to be calculated outside the UI thread, since string formatting is expensive.\r\n- **[Found a extra ComposeView lol](https://github.com/shosetsuorg/shosetsu/commit/891575f2a37f6e8a4613a2c2ddf5c1861a291ee9)**\r\n- **[Use Empty collections where possible](https://github.com/shosetsuorg/shosetsu/commit/f266305953acb1b17af73f09eda91434245e1cfb)** I was seeing a lot of empty collections being made and each of those while dont take much space, have a location in memory. Using the empty collection functions removes those extra allocations.\r\n- **[Improve performance of chapter lists](https://github.com/shosetsuorg/shosetsu/commit/57a3e0bab50dc7f303b79be1950530432e987fef)** by using pre-calculated values for the same reason I added the UI models.\r\n- **[Dont remember derivedStateOf](https://github.com/shosetsuorg/shosetsu/commit/ac30b4929c8aa50a3cd4b9474069ef1440fba311)** derivedStateOf needs to watch values outside the remember function, remembering a derivedStateOf only works if it can directly access the mutableStateOf of the variables\r\n- [**Set MutableStateFlow.value instead of .emit**](https://github.com/shosetsuorg/shosetsu/commit/124ddaae243b95ba9d34ee8bffb9f09ed062d99d) MutableStateFlow is made for watching a state of a value, if you set .value it will first check if its equal to the last value and only emit the new value if its not(since it always emits the latest value on collect, and .emit doesnt set the value, it can emit a old value by accident). You shouldn't use .emit or .tryEmit on a MutableStateFlow, if you need a flow where you can emit independent of the previous value, while keeping track of the last value, you should be using a MutableSharedFlow with a replay value of 1.",
        "issue_html_link": "https://github.com/shosetsuorg/shosetsu/pull/235",
        "issue_url": "https://api.github.com/repos/shosetsuorg/shosetsu/issues/235",
        "CommitDetails": " Before the change, the method downloads chapters if there are any available, and starts downloading worker if a flag is set. After the change, if there are no chapters to download, the method does not perform any further actions.</s>"
        
        Here is the info of issue 2: "issue_index": 234,
        "issue_title": "[F-R] Chapter range download",
        "issue_body": "**Is your feature request related to a problem? Please describe.**\nYes, downloads will be limited to 999 chapters (based on my understanding of the new update).\n\n**Describe the solution you'd like**\nIn the 'download' menu, add \"range download.\" This way, we can download chapters 1 thru 999, then after that is finished, we can download chapter 1000 thru 1998, and so on until all chapters are downloaded.\n\n**Describe alternatives you've considered**\nHit download unread. If limited to 999, then write down your current chapter number(ex: chapter 41) then mark all your downloaded chapters as read, and repeat the process until all chapters are downloaded. Then mark  whatever you didn't read, as unread(ex: selecting chapter 41 thru 2176, and marking them as unread)\n\n**Additional context**\nIf the downloads are limited to 999 maximum downloads, then having this feature would improve convenience of the app.\n",
        "issue_html_link": "https://github.com/shosetsuorg/shosetsu/issues/234",
        "issue_url": "https://api.github.com/repos/shosetsuorg/shosetsu/issues/234",
        "CommitDetails": " I'm unable to directly see or understand the code you've provided. Please give a meaningful description or context of the changes instead, so I can summarize the alteration in one line. For example, \"Before changes: method returned a single value, After changes: method now returns an array.\"</s>"
        
                        
                    OUTPUT: 20%.

                        Another example:
                        INPUT:
                     Here is the info of issue 1:  "issue_index": 232,
        "issue_title": "[Bug] [2.0.0-2344] Migrate source button malfunctioning",
        "issue_body": "**Describe the bug**\r\nThe menu button to migrate a novel's source to a another source seems to be broken.\r\n\r\n**To Reproduce**\r\nSteps to reproduce the behavior:\r\n1. Open Shosetsu\r\n2. Install at least two extensions\r\n3.  Add a novel (a novel within both shouldn't be necessary)\r\n4. Enter the added novel's chapter list view\r\n5. Click or tap the overflow menu within the novel chapter list view\r\n6. Click or tap the \"Migrate source\" overflow menu option\r\n7. Experience the suck. Then embrace the suck. A worldview needed for almost everything in life for those who experience sucky situations or events.\r\n\r\n**Expected behavior**\r\nThe expected behavior is for the user to be able to migrate sources for a novel without experiencing setbacks.\r\n\r\n**Screenshots**\r\nI'm getting tired from typing extra details... it should be fine.... maybe?\r\n\r\n**Device information:**\r\n - OS: Android 10 \r\n - App Version: 2.0.0-2344\r\n\r\n**Additional context**\r\nAdditional context: As my grandpappy always said, \"What a load of bullshit!\"\r\n",
        "issue_html_link": "https://github.com/shosetsuorg/shosetsu/issues/232",
        "issue_url": "https://api.github.com/repos/shosetsuorg/shosetsu/issues/232",
        "CommitDetails": ""
        
        Here is the info of issue 2: "issue_index": 230,
        "issue_title": "[F-R] Change export backup dialog to be easily understood",
        "issue_body": "**Is your feature request related to a problem? Please describe.**\r\nThe export dialog currently seems to not fit the function it enacts. \r\n\r\n**Describe the solution you'd like**\r\nChange the export dialog from \"Export location\" to something along the lines of \"Select backup\"\r\nor \"Select backup to export\"\r\n\r\n**Describe alternatives you've considered**\r\nI believe there isn't a sufficient alternative to this enhancement suggestion.\r\n\r\n**Additional context**\r\nI believe this enhancement report is sufficiently explained.\r\n",
        "issue_html_link": "https://github.com/shosetsuorg/shosetsu/issues/230",
        "issue_url": "https://api.github.com/repos/shosetsuorg/shosetsu/issues/230",
        "CommitDetails": ""
                    OUTPUT: 10%.
                    
                    
                    The similarity in the mapping of the issue and commit must be given as a percentage only. Do not use any common language words to describe their similarity. We need asnwer only in percentages.

    	 
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
    answer = extract_number(temp[len(temp)- 1])
    print("\n\n\n\n\n numerical number" + answer + "\n\n\n\n\n")
    return int(answer)

from dsu import DSU

def issue_issue_map_fun(issue_commits_arr):
    # issue_commits_arr : has issues title, body, and all matching commits summarizations
    n = len(issue_commits_arr)
    mp = {}
    union_find = DSU(n)
    matrix = [[0 for _ in range(n+1)] for _ in range(n+1)]
    for i in range(n):
        mp[issue_commits_arr[i]['issue_index']] = i
    for i in range(min(100, n)):
        for j in range(i+1, min(100, n)):
            percent_match = find_issue_match_percent(issue_commits_arr, i, j)
            issue_num_i = issue_commits_arr[i]['issue_index']
            issue_num_j = issue_commits_arr[j]['issue_index']
            matrix[issue_num_i][issue_num_j] = percent_match
            matrix[issue_num_j][issue_num_i] = percent_match
            with open("issues_issue_match_percent.json", 'w') as f:
                json.dump(matrix, f)
                
            # x = mp[issue_num_i]
            # y = mp[issue_num_j]
            
            # if precent_match > 5:
            #     union_find.union(x,y)
                

        
    return union_find, mp
                
                
import json
with open("issues_commit_summarization.json",'r') as f:
    data = json.load(f)
    data = list(data)
    ds, mp = issue_issue_map_fun(data)
    n = len(data)
    print(mp)
    for i in range(n):
        print("Element {}: Representative = {}".format(i, ds.find(i)))
