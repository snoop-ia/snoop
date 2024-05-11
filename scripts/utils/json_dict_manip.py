import json


def save_dict_as_json(dict_data: dict, file_path: str):
    with open(file_path, "w") as json_file:
        json.dump(dict_data, json_file)
    print(f"Data saved in {file_path}")


def insert_dict_between_keys(original_dict: dict, key_before: str, key_after: str, new_dict: dict) -> dict:
    if key_before not in original_dict or key_after not in original_dict:
        raise ValueError("Both keys must exist in the original dictionary.")

    keys = list(original_dict.keys())
    if keys.index(key_before) >= keys.index(key_after):
        raise ValueError("key_before must be before key_after in the dictionary.")

    # Find the positions for splitting
    pos_before = keys.index(key_before) + 1
    pos_after = keys.index(key_after)

    # Divide into two parts
    first_part = {k: original_dict[k] for k in keys[:pos_after]}
    second_part = {k: original_dict[k] for k in keys[pos_after:]}

    # Merge the dictionaries
    new_dict_ordered = {**first_part, **new_dict, **second_part}

    return new_dict_ordered
