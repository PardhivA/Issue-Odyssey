from dsu import DSU

issue_similarity ={'1': '100', '2': '100', '3':'100', '4':'100', '5':'100', '6': '100'}

issue_related_issue = {'1': '4', '2': '4', '3':'3', '4':'4', '5':'6', '6': '6'}


n = len(issue_commits_arr)
mp = {}
union_find = DSU(n)
for i in range(n):
    mp[issue_commits_arr[i]['issue_index']] = i
    
    percent_match=5
    if percent_match>4:
        #we have i, j matching with each other with 80 % consider
        # so union find completely changes and we have to store all that change in issue_realted_issue
        #but hte problem comes here is that the issue_similarity changes might not be possible
        # becuase we cannot possibly calculate the changed values
        # so i am proposing to not change the similarity of issue
        # FOR EXAMPLE
        #if 1 and 2 were matched initially and they have 1:80% 2;100%(with itself)
        #now if 2 matches with 4 then 2:70% and 4:100% so now  
        pass