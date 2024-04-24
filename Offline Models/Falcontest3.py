from transformers import AutoTokenizer, AutoModelForCausalLM

# Load model and tokenizer
model_name = "tiiuae/falcon-40b-instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Story prompt
prompt = "Write a story about a robot who discovers a hidden world in the jungle."

# Generate text with maximum length of 300 words
sequences = model.generate(
    tokenizer(prompt, return_tensors="pt"),
    max_length=300,
    num_return_sequences=1  # How many stories to generate
)

# Decode the generated text
story = tokenizer.decode(sequences[0], skip_special_tokens=True)

# Print the story
print(story)
