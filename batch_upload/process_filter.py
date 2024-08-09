import csv
from cms_upload import process_entry

def read_input(input_file):
    data = []
    with open(input_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)

    sorted_data = sorted(data, key=lambda x: x['updateAt'])
    return sorted_data

def initial_5w_upload(ori_data):
    data = ori_data[14:50000]
    #data = ori_data[:50]
    count = 14
    for item in data:
        res = process_entry(item)
        print(res)
        count = count + 1
        print(f"Uploaded count: {count}")

def daily_1000_upload(data, start):
    data = ori_data[start:start+1000]
    count = 0
    for item in data:
        res = process_entry(item)
        print(res)
        count = count + 1
        print(f"Uploaded count: {count}")

if __name__ == "__main__":

    input_file = "filter.csv"
    data = read_input(input_file)

    initial_5w_upload(data)

    #daily_1000_upload(data, 50000)
