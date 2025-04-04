import csv
import json
import os
from urllib.parse import urljoin


def absolute_url(base_url:str,relative_url:str) -> str:
    return urljoin(base_url, relative_url)


def save_list_to_csv_and_json(filename, data_list):
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(current_script_dir)
    data_folder = os.path.join(project_dir, 'data')
    os.makedirs(data_folder, exist_ok=True)

    csv_file_path = os.path.join(data_folder, f"{filename}.csv")
    json_file_path = os.path.join(data_folder, f"{filename}.json")

    with open(csv_file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data_list)

    with open(json_file_path, 'w', encoding='utf-8') as file:
        json.dump(data_list, file, indent=4, ensure_ascii=False)


def extract_number(text):
    try:
        start = text.find('(')
        if start == -1:
            return 0

        end = text.find(' ', start)

        if end == -1:
            return 0

        number_in_str = text[start + 1:end]

        return int(number_in_str)
    except (ValueError, IndexError) as e:
        print(f"Error extracting number: {e}")
        return -1