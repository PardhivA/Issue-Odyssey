from transformers import AutoModelForCausalLM, AutoTokenizer

device = "cpu" # the device to load the model onto

model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")
tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")

messages=[{
                    'role': 'user',
                    'content': ''' You will receive two objects. One is the lines of code of a method before changes due to a commit and second one is also some lines of code of a method after changes, your job is to give me a one line summarization of what is altered and the meaning of it based on the before and after the method changes, only one line summarization
                    ''',
                },{
                    'role': 'assistant',
                    'content': 'ok',
                },
                {
                     'role': 'user',
                    'content': '''
        method before: 
                    override fun openLastRead(): Flow<ChapterUI?> =
		flow {
			val array = chaptersFlow.first()
			val sortedArray = array.sortedBy { it.order }
			val result = isChaptersResumeFirstUnread()

			val index: Int = if (!result)
				sortedArray.indexOfFirst { it.readingStatus != ReadingStatus.READ }
			else sortedArray.indexOfFirst { it.readingStatus == ReadingStatus.UNREAD }
			

			emit(
				if (index == -1) {
					null
				} else {
					itemIndex.emit(index + 1) // +1 to account for header
					sortedArray[index]
						}
			)
		}.onIO()


        method after: 
        		override fun openLastRead(): Flow<ChapterUI?> =
		flow {
			val array = chaptersFlow.first()
			val sortedArray = array.sortedBy { it.order }
			val result = isChaptersResumeFirstUnread()
			val item = if (!result)
			sortedArray.firstOrNull { it.readingStatus != ReadingStatus.READ }
			else sortedArray.firstOrNull { it.readingStatus == ReadingStatus.UNREAD }
			emit(
			if (item == null) {
					null
				} else {
					itemIndex.emit(array.indexOf(item) + 1) // +1 to account for header
					item
				}
			)
		}.onIO()
                    ''',
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
print("summarization: ", temp[len(temp)- 1])