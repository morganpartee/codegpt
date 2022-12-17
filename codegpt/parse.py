def parse_resp(response:dict):
    resp = response["choices"][0]["text"].splitlines()
    
    # Initialize an empty list to hold the dictionaries
    out = []

    # Initialize an empty dictionary to hold the current key-value pairs
    curr_dict = {}

    # Iterate through each line in the response
    for line in resp:
        line = line.strip()
        # Skip empty lines
        if not line:
            continue

        # If the line doesn't start with '>', it's a key
        if line[0] != '>':
            if line == '===' and curr_dict:
                out.append(curr_dict)
                curr_dict = {}
            # Strip leading/trailing whitespace and remove ':' from the key
            key = line.strip().replace(":", '')
            # Initialize an empty value for this key in the current dictionary
            curr_dict[key] = ""
        # If the line does start with '>', it's a value
        else:
            # Strip the leading '>' and leading/trailing whitespace from the value
            # and add it to the current key in the current dictionary
            if key == "code":
                curr_dict[key] += line.strip().strip('> ').strip('>') + '\n'
            else:
                curr_dict[key] = line.strip().strip('> ').strip('>').strip()

    # Add the final dictionary to the output list
    out.append(curr_dict)

    return out