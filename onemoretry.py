from transformers import AutoTokenizer, AutoModel
import torch
from scipy.spatial.distance import cosine

def semantic_similarity(str1, str2, model_name='distilbert-base-nli-stsb-mean-tokens'):
    """
    Calculate semantic similarity between two strings using pre-trained models.
    
    Args:
    - str1 (str): First string.
    - str2 (str): Second string.
    - model_name (str): Name or path of the pre-trained model to use. 
                        Default is 'distilbert-base-nli-stsb-mean-tokens'.
    
    Returns:
    - float: Similarity score between 0 and 1. 
             1 means the strings are semantically identical, 
             0 means they have no semantic similarity.
    """
    # Load pre-trained model and tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)
    
    # Tokenize input strings
    inputs = tokenizer([str1, str2], return_tensors='pt', padding=True, truncation=True)
    
    # Get model embeddings
    with torch.no_grad():
        outputs = model(**inputs)
        embeddings = torch.mean(outputs.last_hidden_state, dim=1)
    
    # Calculate cosine similarity between the embeddings
    similarity_score = 1 - cosine(embeddings[0], embeddings[1])
    
    return similarity_score

# Example usage:
string1 = "The quick brown fox jumps over the lazy dog."
string2 = "A fast fox jumps over a lazy dog."
similarity = semantic_similarity(string1, string2)
print(f"Semantic similarity score: {similarity}")
