import tensorflow_hub as hub
import tensorflow_text

def semantic_similarity(str1, str2):
    """
    Calculate semantic similarity between two strings using Universal Sentence Encoder (USE).
    
    Args:
    - str1 (str): First string.
    - str2 (str): Second string.
    
    Returns:
    - float: Similarity score between -1 and 1. 
             1 means the strings are semantically identical, 
             -1 means they have no semantic similarity.
    """
    # Load Universal Sentence Encoder
    embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder-multilingual/3")
    
    # Compute embeddings
    embeddings = embed([str1, str2])
    
    # Calculate cosine similarity
    similarity_score = float(embeddings[0].numpy().dot(embeddings[1].numpy()) / (np.linalg.norm(embeddings[0].numpy()) * np.linalg.norm(embeddings[1].numpy())))
    
    return similarity_score

# Example usage:
string1 = "The quick brown fox jumps over the lazy dog."
string2 = "A fast fox jumps over a lazy dog."
similarity = semantic_similarity(string1, string2)
print(f"Semantic similarity score: {similarity}")
