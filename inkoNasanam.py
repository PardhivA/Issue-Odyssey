from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cosine

def semantic_similarity(str1, str2, model_name='paraphrase-distilroberta-base-v2'):
    """
    Calculate semantic similarity between two strings using pre-trained models.
    
    Args:
    - str1 (str): First string.
    - str2 (str): Second string.
    - model_name (str): Name of the pre-trained model to use. Default is 'paraphrase-distilroberta-base-v2'.
    
    Returns:
    - float: Similarity score between 0 and 1. 
             1 means the strings are semantically identical, 
             0 means they have no semantic similarity.
    """
    # Load pre-trained model
    model = SentenceTransformer(model_name)
    
    # Encode sentences into semantic vectors
    embeddings = model.encode([str1, str2])
    
    # Calculate cosine similarity between the embeddings
    similarity_score = 1 - cosine(embeddings[0], embeddings[1])
    
    return similarity_score

# Example usage:
string1 = "**Describe the bug**\r\n\r\nMy journal is being spammed with:\r\n\r\n```\r\nAug 24 11:24:21 pc.example.com gnome-shell[1840277]: g_signal_handler_disconnect: assertion 'handler_id > 0' failed\r\nAug 24 11:24:21 pc.example.com gnome-shell[1840277]: g_signal_handler_disconnect: assertion 'handler_id > 0' failed\r\nAug 24 11:24:21 pc.example.com gnome-shell[1840277]: g_signal_handler_disconnect: assertion 'handler_id > 0' failed\r\nAug 24 11:24:21 pc.example.com gnome-shell[1840277]: g_signal_handler_disconnect: assertion 'handler_id > 0' failed\r\nAug 24 11:24:21 pc.example.com gnome-shell[1840277]: g_signal_handler_disconnect: assertion 'handler_id > 0' failed\r\nAug 24 11:24:21 pc.example.com gnome-shell[1840277]: g_signal_handler_disconnect: assertion 'handler_id > 0' failed\r\nAug 24 11:24:21 pc.example.com gnome-shell[1840277]: g_signal_handler_disconnect: assertion 'handler_id > 0' failed\r\nAug 24 11:24:21 pc.example.com gnome-shell[1840277]: g_signal_handler_disconnect: assertion 'handler_id > 0' failed\r\nAug 24 11:24:21 pc.example.com gnome-shell[1840277]: g_signal_handler_disconnect: assertion 'handler_id > 0' failed\r\nAug 24 11:24:21 pc.example.com gnome-shell[1840277]: g_signal_handler_disconnect: assertion 'handler_id > 0' failed\r\nAug 24 11:24:21 pc.example.com gnome-shell[1840277]: g_signal_handler_disconnect: assertion 'handler_id > 0' failed\r\n\r\n```\r\n\r\n**Steps To Reproduce:**\r\n\r\nNot really sure of any specific steps, but enabling/disabling GSConnect makes this happen/not happen.\r\n\r\n**Expected behavior**\r\n\r\nShould not be spamming the journal with an assertion.\r\n\r\n**System Details (please complete the following information):**\r\n\r\n - **GSConnect version:** 50\r\n   - **Installed from:** Fedora 36 RPM\r\n - **GNOME/Shell version:** 42.4\r\n - **Distro/Release:** Fedora 36\r\n\r\n**GSConnect environment (if applicable):**\r\n\r\n - **Paired Device(s):** Lineage 19.1 phone and Honor 8\r\n - **KDE Connect app version:** 1.19.1\r\n - **Plugin(s):** N/A"
string2 = "Since GNOME 42, the popup menu uses `connectObject()` instead of storing\r\nthe handler ID on the item.\r\n\r\nGet the handler ID with `GObject.signal_handler_find()` and connect the\r\nreplacement with `connectObject()`.\r\n\r\nfixes #1442"
similarity = semantic_similarity(string1, string2)
print(f"Semantic similarity score: {similarity}")
