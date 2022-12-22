def parse_resp(response:dict):
    resp = response["choices"][0]["text"].strip().splitlines()

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
            # Strip leading/trailing whitespace and remove ':' from the key
            key = line.strip().replace(":", '').lower()
            # Initialize an empty value for this key in the current dictionary
            curr_dict[key] = ""
        else:
            curr_dict[key] += line.strip().strip('> ').strip('>') + '\n'

    # Add the final dictionary to the output list
    out.append(curr_dict)

    return out