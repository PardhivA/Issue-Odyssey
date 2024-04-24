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
    print("askingMistrak",i, j)
    # print(temp)
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
    union_find = DSU(n)
    for i in range(n):
        mp[issue_commits_arr[i]['issue_index']] = i
    
    with open("map_of_issue_to_number_complex.json",'w') as wrwr:
        json.dump(mp, wrwr)
    
    issue_and_related_issue = {}
    for i in range(n):
        print("cuyrrent i", i)
        current_issue_number = mp[issue_commits_arr[i]['issue_index']]
        if(str(current_issue_number) not in issue_and_related_issue):
            issue_and_related_issue[current_issue_number] = {"issueNumber": current_issue_number, "similarity_percentage": str(100)}
        for j in range(i+1, n):
            print("cuyrrent j", j)
            percent = find_issue_match_percent(issue_commits_arr, i, j)
            issue_num_i = issue_commits_arr[i]['issue_index']
            issue_num_j = issue_commits_arr[j]['issue_index']
            x = mp[issue_num_i]
            y = mp[issue_num_j]
            print(x,"==",issue_num_i,"   ", issue_num_j,"==" ,y, "  ===>  ",percent)
            if percent > 60:
                union_find.union(x,y)
                issue_and_related_issue[y] = {"issueNumber": union_find.find(y), "similarity_percentage": str(percent)}
                issue_and_related_issue[x] = {"issueNumber": union_find.find(x), "similarity_percentage": str(percent)}
                with open("relation_issue_issue_complex.json",'w') as iir:
                    json.dump(issue_and_related_issue, iir)
                
    return union_find, mp



                
import json
import os
# with open("SWELinker30/issues_commit_summarization_individual.json",'r') as f:

#     data = json.load(f)
#     data = list(data)
    
a = None
with open("/home/ssl31/Downloads/SWELinker30/issues_commit_summarization_individual.json") as f:
    a = json.load(f)
b = a.copy()
for issue in b:
    k = ""
    for commit in issue["CommitDetails"]:
        k += commit["method_summarization"]
    issue["Commit summary"] = k
    del issue["CommitDetails"]
    
print("did something here")
with open("./test1.json","w") as out:
    json.dump(b,out)


# print(len(b), b[0])
    
ds, mp = issue_issue_map_fun(b)
n = len(b)
print(mp)


# for i in range(n):
#     print("Element {}: Representative = {}".format(i, ds.find(i)))
        

