# pip install 'transformers @ git+https://github.com/huggingface/transformers.git@831bc25d8fdb85768402f772cf65cc3d7872b211'
# pip install accelerate

import torch
from transformers import pipeline

pipe = pipeline(
    "text-generation",
    model="HuggingFaceH4/starchat2-15b-v0.1",
    device_map="auto",
    torch_dtype=torch.bfloat16,
)
messages = [
    {
        "role": "system",
        "content": "You are StarChat2, an expert programming assistant",
    },
    {"role": "user", "content": "Write a simple website in HTML. When a user clicks the button, it shows a random Chuck Norris joke."},
]
outputs = pipe(
    messages,
    max_new_tokens=512,
    do_sample=True,
    temperature=0.7,
    top_k=50,
    top_p=0.95,
    stop_sequence="<|im_end|>",
)
print(outputs[0]["generated_text"][-1]["content"])

