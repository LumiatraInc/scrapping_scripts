import json

def write_to_json_file(data: list[dict], file_name: str = "business.json",):
    with open(file_name, "w") as file:
        file.write("[")
        for index, business in enumerate(data):
            if index == (len(data) - 1):
                line = json.dumps(business)
            else:
                line = json.dumps(business) + ",\n"
            file.write(line)
        file.write("]")

