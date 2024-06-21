import json

def write_to_json_file(data: list[dict], file_name: str = "business.json",):
    with open(file_name, "w", encoding="utf-8") as file:
        file.write("[")
        for index, business in enumerate(data):
            if index == (len(data) - 1):
                line = json.dumps(business)
            else:
                line = json.dumps(business) + ",\n"
            file.write(line)
        file.write("]")


def create_open_json_file(file_name: str = "business.json"):
    with open(file_name, "w", encoding="utf-8") as file:
        file.write("[\n")

def close_json_file(file_name: str = "business.json"):
    with open(file_name, "a", encoding="utf-8") as file:
        file.write("]\n")

def write_to_opened_json_file(file_name: str = "business.json", business_data: dict = {}, end_file: bool = False):
    with open(file_name, "a", encoding="utf-8") as file:
        if not end_file:
            data = json.dumps(business_data, ensure_ascii=False) + ",\n"
        else:
            data = json.dumps(business_data, ensure_ascii=False)
        file.write(data)

