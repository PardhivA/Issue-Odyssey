from transformers import AutoModelForCausalLM, AutoTokenizer

device = "cpu" # the device to load the model onto

model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")
tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")

messages=[{
                    'role': 'user',
                    'content': ''' You will receive two objects. One is the lines of code of a method before changes due to a commit and second one is also some lines of code of a method after changes, your job is to give me a one line summarization of  the alteration (not interms of code but in terms of meaning) based on the before and after the method changes, only one line summarization
                    ''',
                },{
                    'role': 'assistant',
                    'content': 'ok',
                },
                {
                     'role': 'user',
                    'content': '''
        method before: 
                    override fun FastAdapter<AbstractItem<*>>.setupFastAdapter() {
		selectExtension {
			isSelectable = true
			multiSelect = true
			selectOnLongClick = true
			setSelectionListener { item, _ ->
            // Recreates the item view
				this@setupFastAdapter.notifyItemChanged(this@setupFastAdapter.getPosition(item))
            	// Swaps the options menu on top
				val size = selectedItems.size
                if (size == 1) startSelectionAction() else if (size == 0) finishSelectionAction()
			}
		}

        method after: 
    override fun FastAdapter<AbstractItem<*>>.setupFastAdapter() {
		selectExtension {
			isSelectable = true
			multiSelect = true
			selectOnLongClick = true
            setSelectionListener { item, isSelected ->
				// Recreates the item view
				this@setupFastAdapter.notifyItemChanged(this@setupFastAdapter.getPosition(item))
            // Swaps the options menu on top
				val size = selectedItems.size

				// Incase the size is empty and the item is selected, add the item and try again
				if (size == 0 && isSelected) {
					logE("Migrating selection bug")
					(fastAdapter.getItemById(item.identifier)?.first as? ChapterUI)?.isSelected =
						true
					this.select(item, true)
					return@setSelectionListener
				}

				if (size == 1) startSelectionAction() else if (size == 0) finishSelectionAction()
			}
		}
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