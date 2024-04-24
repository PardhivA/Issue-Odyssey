from transformers import AutoModelForCausalLM, AutoTokenizer, set_seed
import torch
torch.set_default_tensor_type(torch.cuda.FloatTensor)
model_ID = "bigscience/bloom-7b1"
model = AutoModelForCausalLM.from_pretrained(model_ID, use_cache=False)
tokenizer = AutoTokenizer.from_pretrained(model_ID)
set_seed(2024)
story_title = 'An Unexpected Journey Through Time'
prompt = f'What is the first programming language ever invented ?.\n'
input_ids = tokenizer(prompt, return_tensors="pt").to(0)

sample = model.generate(**input_ids,
                        max_length=200, top_k=1,
                        temperature=0, repetition_penalty=2.0)

generated_story = tokenizer.decode(sample[0], skip_special_tokens=True)
import textwrap
wrapper = textwrap.TextWrapper(width=80)
formated_story = wrapper.fill(text=generated_story)
print(formated_story)