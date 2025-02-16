import json

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def compare_json(file1, file2):
    json1 = load_json(file1)
    json2 = load_json(file2)
    return json1 == json2


def sort_values(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, list):
                data[key] = sorted(value)
            elif isinstance(value, dict):
                sort_values(value)
    elif isinstance(data, list):
        for item in data:
            sort_values(item)

def compare_json_files(file1_path, file2_path):
    with open(file1_path, 'r', encoding='utf-8') as file1:
        data1 = json.load(file1)
    with open(file2_path, 'r', encoding='utf-8') as file2:
        data2 = json.load(file2)

    sort_values(data1)
    sort_values(data2)

    return data1 == data2