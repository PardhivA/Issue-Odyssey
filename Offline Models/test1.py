from transformers import AutoModelForCausalLM, AutoTokenizer

device = "cpu" # the device to load the model onto

model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")
tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")


messages=[{
                    'role': 'user',
                    'content': '''Given an issue's details and a  commit's method change summarization, give me a percentage of similartity that the commit is made to solve that issue.  No other text should be given. Here are some examples
						issue_title: "[Bug] [2186]'Teleportation' to chapter when you click the resume button is wrong if the sort is the oppisite"
                        issue_body: "https://user-images.githubusercontent.com/75091899/170125379-289b87c2-a4be-4a93-bab1-67885cf3815c.mp4\r\n\r\nidk how to descrive it but here is the video\r\n\r\n**To Reproduce**\r\nSteps to reproduce the behavior:\r\n1. pick a novel with a lot of chapters\r\n2. mark as read 2/3 of the total amount\r\n3. reverse the sort direction of chapters\r\n4. click resume button\r\nyou will see for a second that tha app teleported to the wrong chapter (it should be the last read one 1004, but it teleporter at the end of the video to 473, visually)\r\n\r\n**Expected behavior**\r\nthe app teleported to the wrong chapter (visually) but it opened the right chapter so the bug is that the short animation where the app teleport to the actual chapter is wrong if the sort direction is the opposite from the default one\r\n\r\n**Screenshots**\r\nIf applicable, add screenshots to help explain your problem.\r\n\r\n**Device information:**\r\n - OS:  android 8\r\n - App Version: r2186\r\n\r\n**Additional context**\r\nAdd any other context about the problem here.\r\n"
                        commit_summarization: In the altered method, instead of using `indexOfFirst` to get the index of the first unread or unread chapter, the method uses `firstOrNull` to retrieve the first occurrence of an unread/unread chapter, and assigns the index of that chapter to the output variable.
                        
                        The percentage of similarity for this issue and commit summarization is 100.

                        Another example:
                    issue_title: "Move app package to app.shosetsu.android"
                    issue_body: null
                    commit_summarization: "The change introduces the loading of extensions from a repository before restoring them, allowing for dynamic retrieval and modification of extensions"
                  
                    The percentage of similarity for this issue and commit summarization is 50.
                    Another example:
                    issue_title: "[Bug] [2.0.0-2344] Migrate source button malfunctioning"
                    issue_body: "**Describe the bug**\r\nThe menu button to migrate a novel's source to a another source seems to be broken.\r\n\r\n**To Reproduce**\r\nSteps to reproduce the behavior:\r\n1. Open Shosetsu\r\n2. Install at least two extensions\r\n3.  Add a novel (a novel within both shouldn't be necessary)\r\n4. Enter the added novel's chapter list view\r\n5. Click or tap the overflow menu within the novel chapter list view\r\n6. Click or tap the \"Migrate source\" overflow menu option\r\n7. Experience the suck. Then embrace the suck. A worldview needed for almost everything in life for those who experience sucky situations or events.\r\n\r\n**Expected behavior**\r\nThe expected behavior is for the user to be able to migrate sources for a novel without experiencing setbacks.\r\n\r\n**Screenshots**\r\nI'm getting tired from typing extra details... it should be fine.... maybe?\r\n\r\n**Device information:**\r\n - OS: Android 10 \r\n - App Version: 2.0.0-2344\r\n\r\n**Additional context**\r\nAdditional context: As my grandpappy always said, \"What a load of bullshit!\"\r\n"
                    commit_summarization: "The change introduces the loading of extensions from a repository before restoring them, allowing for dynamic retrieval and modification of extensions"
                  
                    The percentage of similarity for this issue and commit summarization is 0.
                    
    	 
                       ''',
                },{
                    'role': 'assistant',
                    'content': 'ok',
                },
                {
                    'role': 'user',
                    'content': '''
        Output should be given in this format: "The percentage is x%.".
        Here is the info:
        
        issue_title: "[Bug] [r1136] Chapter selection bugs out"
        issue_body: "**Describe the bug**\nSometimes, when trying to select a chapter with a long press, it won't select. Other times, it'll require a second long press\n\n**To Reproduce**\nSteps to reproduce the behavior:\n1. Click on a novel\n2. Long press a chapter\n3.  Now it's hit or miss. It may work immediately, it may take a retry to select, or it may not work at all\n\n**Expected behavior**\nChapter to be selected on the first try\n\n**Device information:**\n - OS: Android 10\n - App Version: r1136\n\n**Additional context**\nI believe the bug happens more often if you've used the select function a few times for other novels. For example , Astral Pet Store selecting chapter 1-200 then hitting mark read, do the same with chrysalis, then it is hit or miss weather it'll work on the next, after five it stops working entirely\n"
        summarization: The method alteration adds error handling to prevent a selection bug when an item is long pressed during a selection process with an empty selection list.            
                        ''',
				}
                ]

encodeds = tokenizer.apply_chat_template(messages, return_tensors="pt")
model_inputs = encodeds.to(device)
model.to(device)
generated_ids = model.generate(model_inputs, max_new_tokens=1000, do_sample=True)
decoded = tokenizer.batch_decode(generated_ids)
print("summirization: ", decoded[0])