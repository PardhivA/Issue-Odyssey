import Levenshtein

def string_similarity(str1, str2):
    """
    Calculate similarity ratio between two strings using Levenshtein distance.
    
    Args:
    - str1 (str): First string.
    - str2 (str): Second string.
    
    Returns:
    - float: Similarity ratio between 0 and 1. 
             1 means the strings are identical, 
             0 means they have no similarity.
    """
    distance = Levenshtein.distance(str1, str2)
    max_len = max(len(str1), len(str2))
    similarity_ratio = 1 - (distance / max_len)
    return similarity_ratio

# Example usage:
string1 = "**Describe the bug**\r\n\r\nMy journal is being spammed with:\r\n\r\n```\r\nAug 24 11:24:21 pc.example.com gnome-shell[1840277]: g_signal_handler_disconnect: assertion 'handler_id > 0' failed\r\nAug 24 11:24:21 pc.example.com gnome-shell[1840277]: g_signal_handler_disconnect: assertion 'handler_id > 0' failed\r\nAug 24 11:24:21 pc.example.com gnome-shell[1840277]: g_signal_handler_disconnect: assertion 'handler_id > 0' failed\r\nAug 24 11:24:21 pc.example.com gnome-shell[1840277]: g_signal_handler_disconnect: assertion 'handler_id > 0' failed\r\nAug 24 11:24:21 pc.example.com gnome-shell[1840277]: g_signal_handler_disconnect: assertion 'handler_id > 0' failed\r\nAug 24 11:24:21 pc.example.com gnome-shell[1840277]: g_signal_handler_disconnect: assertion 'handler_id > 0' failed\r\nAug 24 11:24:21 pc.example.com gnome-shell[1840277]: g_signal_handler_disconnect: assertion 'handler_id > 0' failed\r\nAug 24 11:24:21 pc.example.com gnome-shell[1840277]: g_signal_handler_disconnect: assertion 'handler_id > 0' failed\r\nAug 24 11:24:21 pc.example.com gnome-shell[1840277]: g_signal_handler_disconnect: assertion 'handler_id > 0' failed\r\nAug 24 11:24:21 pc.example.com gnome-shell[1840277]: g_signal_handler_disconnect: assertion 'handler_id > 0' failed\r\nAug 24 11:24:21 pc.example.com gnome-shell[1840277]: g_signal_handler_disconnect: assertion 'handler_id > 0' failed\r\n\r\n```\r\n\r\n**Steps To Reproduce:**\r\n\r\nNot really sure of any specific steps, but enabling/disabling GSConnect makes this happen/not happen.\r\n\r\n**Expected behavior**\r\n\r\nShould not be spamming the journal with an assertion.\r\n\r\n**System Details (please complete the following information):**\r\n\r\n - **GSConnect version:** 50\r\n   - **Installed from:** Fedora 36 RPM\r\n - **GNOME/Shell version:** 42.4\r\n - **Distro/Release:** Fedora 36\r\n\r\n**GSConnect environment (if applicable):**\r\n\r\n - **Paired Device(s):** Lineage 19.1 phone and Honor 8\r\n - **KDE Connect app version:** 1.19.1\r\n - **Plugin(s):** N/A"
# string1 = "g_signal_handler_disconnect: assertion 'handler_id > 0' failed"
# string2 = "gmenu: fix assertion when disconnecting signal"
string2 = "Since GNOME 42, the popup menu uses `connectObject()` instead of storing\r\nthe handler ID on the item.\r\n\r\nGet the handler ID with `GObject.signal_handler_find()` and connect the\r\nreplacement with `connectObject()`.\r\n\r\nfixes #1442"
similarity = string_similarity(string1, string2)
print(f"Similarity ratio: {similarity}")