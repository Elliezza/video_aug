info_file = "publisher_info.json"
name_file = "names.txt"

def read_info():
    with open(info_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
    return data

def write_info():
    with open(info_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

def get_publish_id(name):

    publishID = 1
    publishName = "Hello"

    data = read_info()
    
    for i in range(len(data[name])):
        key = list(my_dict.keys())[0]
        if data[name][key] < 201:
            publishID = key
            data[name][key] +=1
            break
        else:
            continue

    write_info(data)
    
    return publishID, publishName
