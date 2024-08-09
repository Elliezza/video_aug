import json

info_file = "publisher_info.json"
account_file = "accounts.txt"
record_file = "allocation.json"


def read_info(in_file):
    with open(in_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
    return data

def write_info(out_file, data):
    with open(out_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

def get_id(name):

    data = read_info(info_file)
    import pdb; pdb.set_trace() 
    entry_keys = list(data[name].keys())
    for i in range(len(entry_keys)):
        key = entry_keys[i]
        if data[name][key] < 201:
            publishID = key
            data[name][key] +=1
            break
        else:
            continue

    write_info(info_file, data)
    
    return publishID

def read_txt_file(file_path):
    user_list = []

    # Open the file in read mode
    with open(file_path, 'r') as file:
    # Iterate over each line in the file
        for line in file:
        # Remove any leading/trailing whitespace and split the line by comma
            parts = line.strip().split(',')
        # Append the tuple (id, nickname) to the list
            user_list.append((parts[0], parts[1]))
    return user_list

def get_id_and_names(temp_id):
    users = read_txt_file(account_file)
    allocations = read_info(record_file)

    import pdb; pdb.set_trace()
    if temp_id not in allocations:
        new_id = len(allocations.keys())
        allocations[temp_id] = users[new_id]
        write_info(record_file, allocations)
    
    return allocations[temp_id]

def get_publish_id(name):    
    temp_id = get_id(name)

    return get_id_and_names(temp_id)

