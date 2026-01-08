""" youtube/parser.py
Cleans YouTube inputs and extracts usable identifiers.
"""

import re

def extract_identifier(input_url: str):
    """
    Takes messy inputs (full URLs, handles, raw IDs) 
    returns:
    (clean_identifier, id_type)
    
    id_type = "handle" or "id"
    """

    #Remove trailing spaces and slashes
    input_url = input_url.strip().rstrip('/')

    #Regex to match URLs
    pattern = r'(?:https?://)?(?:www\.)?youtube\.com/(?:@|channel/|c/|user/)?([a-zA-Z0-9\-_.]+)'

    #Case 1: raw handle starting with @
    if input_url.startswith('@'):
        return input_url, "handle"

    #Case 2: URL pattern
    match = re.search(pattern, input_url)
    if match:
        identifier = match.group(1)
        #Channel IDs always start with 'UC' and are 24 chars
        if identifier.startswith('UC') and len(identifier) == 24:
            return identifier, "id"
        else:
            #Ensure handle starts with @
            clean_handle = identifier if identifier.startswith('@') else f"@{identifier}"
            return clean_handle, "handle"

    #Case 3: fallback — assume handle
    return f"@{input_url}" if not input_url.startswith("@") else input_url, "handle"
