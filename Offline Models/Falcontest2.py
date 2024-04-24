from transformers import AutoTokenizer, FalconModel
import torch

tokenizer = AutoTokenizer.from_pretrained("Rocketknight1/falcon-rw-1b")
model = FalconModel.from_pretrained("Rocketknight1/falcon-rw-1b")

inputs = tokenizer("Hello, my dog is cute", return_tensors="pt")
outputs = model(**inputs)

last_hidden_states = outputs.last_hidden_state