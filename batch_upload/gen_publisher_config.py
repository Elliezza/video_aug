import json
import csv
import math

if __name__ == "__main__":
    output_file = "publisher_info.json"
    csv_file = "filter.csv"

    ori_data = []
    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            ori_data.append(row)
    #sort
    data = sorted(ori_data, key=lambda x: x['updateAt'])


    publisher={}
    for item in data:
        if item['publisherName'] not in publisher: # == '锤砸在野':
            publisher[item['publisherName']] = [ item ]
        else:
            publisher[item['publisherName']].append(item)

    publisher_count={}

    for item in data:
        if item['publisherName'] not in publisher_count: # == '锤砸在野':
            publisher_count[item['publisherName']] = 1
        else:
            publisher_count[item['publisherName']] += 1

    sorted_dict_asc = dict(sorted(publisher_count.items(), key=lambda item: item[1]))

    user_id = 1

    config_dict = {}

    for user in publisher_count.keys():
        config_dict[user] = {}
        if publisher_count[user] < 201:
            config_dict[user][user_id]= 0
            user_id +=1
        else: # split into multiple accounts
            number = math.ceil(publisher_count[user]/200)
            for i in range(number):
                config_dict[user][user_id] = 0
                user_id +=1

    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(config_dict, file, indent=4, ensure_ascii=False)  # Pretty-print JSON with indentation
        print(f"Data successfully written to {output_file}")
    except IOError as e:
        print(f"Failed to write to file: {e}")


    import pdb; pdb.set_trace()
