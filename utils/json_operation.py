import json


def save_json(file_name, data_dict):
    data_json = json.dumps(data_dict)
    file = open(file_name, 'w')
    file.write(data_json)
    file.close()


def load_json(file_name):
    file = open(file_name, 'r')
    file_json = json.loads(file.read())
    file.close()
    return file_json
