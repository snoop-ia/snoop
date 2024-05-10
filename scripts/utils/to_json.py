import json


def save_dict_as_json(dict_data, file_path):
    with open(file_path, "w") as json_file:
        json.dump(dict_data, json_file)
    print(f"Data saved in {file_path}")