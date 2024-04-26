
<p align="center">
 <img src="https://github.com/PardhivA/Issue-Odyssey/assets/126562985/905d183a-230e-4b83-b122-3f6ec054d86f" alt="Github Issue Image">
</p>


# Issue Odyssey



Software development projects often face challenges in managing
issues and understanding the evolution of code changes over time.
In this report, we present the development of a tool called "Issue
Odyssey" aimed at addressing these challenges. 
* The tool utilizes commit data to establish connections between related issues within
a code base, offering insights into the life cycle of software issues
and patterns of similarity among them.
* Leveraging large language
models (LLMs) and deep learning techniques, Issue Odyssey provides developers with actionable insights for more targeted issue
resolution efforts and enhances the efficiency of issue management
processes.

## Video Demo


https://github.com/PardhivA/Issue-Odyssey/assets/126562985/ff4ece75-47d7-4f88-87cb-a0f91c0eee1f




[GitHub action]: https://github.com/andresz1/size-limit-action
[Statoscope]:    https://github.com/statoscope/statoscope
[cult-img]:      http://cultofmartians.com/assets/badges/badge.svg
[cult]:          http://cultofmartians.com/tasks/size-limit-config.html



## How It Works (Working Pipeline of the Tool )
![diagram-export-24-04-2024-20_53_58](https://github.com/PardhivA/Issue-Odyssey/assets/126562985/49713d0a-b682-47df-a24b-1215c488210c)



## Usage

### Requirements
```python
pip install pydriller
pip install transformers
pip install torch  
```
### git clone
```
mkdir IssueOdyssey
cd IssueOdyysey
git clone https://github.com/PardhivA/Issue-Odyssey.git
```
### How to start Backend Server 

```
cd ssl31
```
* Now go to API,py, and at line 209

![image](https://github.com/PardhivA/Issue-Odyssey/assets/126562985/6ed2610e-0aa5-4617-88a3-8123affa9848)

* Now, use the IP address at which you want to run the server.

* Now, we shall run the API.py file 
```
python3 API.py
````

#### Note : 
Keep the server ON as long as you are using the extension. 

### Usage of Extension from the Client side
* Open the new terminal in IssueOdyssey folder and then 
```
cd Client
```
* Now go to content.js and at line 416

![image](https://github.com/PardhivA/Issue-Odyssey/assets/126562985/14ef0af7-6092-463e-b4ac-2ae3af314f4c)

* Use the server address and port here.

  *From here, please FOLLOW the video demo ABOVE to use the tool in GitHub.*



## CONCLUSION
Using our tool we were able to achieve our 60% accuracy  in linking issues  with each other. However,  we can improve the performance of the tool by considering the factors below
* **Strengths**: The tool demonstrates the potential in effectively
analyzing code evolution and identifying links between
issues and code commit.
* **Areas for Improvement**: Despite the promising accuracy
rate, there is room for improvement, particularly in enhancing the precision and recall of the tool. Further refinement
of the algorithms and fine-tuning of parameters may lead
to better performance.
* **Future Directions**: Future iterations of the tool could explore additional methodologies and incorporate feedback
mechanisms to continuously improve accuracy and relevance. Moreover, scalability and efficiency enhancements could be prioritized to handle larger datasets and optimize
processing times.









