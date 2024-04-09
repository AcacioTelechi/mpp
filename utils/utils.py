import json

def save_json(folder_name, file_name, obj):
    with open(folder_name + "/" + file_name + ".json", "w", encoding="utf8") as f:
        json.dump(obj, f)