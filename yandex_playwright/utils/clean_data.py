

def clean_data(data: list[dict]) -> list[dict]:
    clean_data: list[dict] = []

    for raw_data in data:
        if raw_data["business_address"] is None:
            continue

        clean_data.append(raw_data)

    return clean_data