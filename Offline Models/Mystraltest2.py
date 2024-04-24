from transformers import AutoModelForCausalLM, AutoTokenizer

checkpoint = "HuggingFaceH4/zephyr-7b-beta"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModelForCausalLM.from_pretrained(checkpoint)

messages = [{
    "role" : "system",
    "content" : "You are a friendly chatbot who always responds in the style of a pirate",
    },
    { "role": "user", "content" : "How many helicopters can a human eat in one sitting?"},
    ]
tokenized_chat=  tokenizer.apply_chat_template(messages, tokenize = True, add_generation_prompt = True, return_tensors = "pt")
print(tokenizer.decode(tokenized_chat[0]))
outputs = model.generate(tokenized_chat, max_new_tokens = 128)
print(tokenizer.decode(outputs[0]))
