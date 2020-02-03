import json
from pathlib import Path


def convert_factbook_json_to_dict(path: Path):
    with open(path, 'r', encoding="utf8") as jsonfile:
        data = json.load(jsonfile)
    return data


def extract_env_data(full_data: dict, output_path):

    env_dict = {}

    for country_name, country in full_data['countries'].items():
        country_dict = {}
        env_issues = []

        try:
            env_issues = country['data']['geography']['environment']['current_issues']
        except KeyError:
            print(f"Key does not exist for country {country_name}")

        country_dict["environmental_issues"] = env_issues
        env_dict[country_name] = country_dict

    with open(output_path, 'w+') as outfile:
        json.dump(env_dict, outfile)


if __name__ == "__main__":
    parent_raw = Path(__file__).parent.parent.parent / 'data' / 'raw'
    parent_processed = Path(__file__).parent.parent.parent / 'data' / 'processed'

    data2007 = parent_raw / 'weekly_json' / '2007-06-18_factbook.json'
    data2019 = parent_raw / 'factbook.json'

    dict2007 = convert_factbook_json_to_dict(data2007)
    dict2019 = convert_factbook_json_to_dict(data2019)

    output2007 = parent_processed / 'env_data_2007.json'
    output2019 = parent_processed / 'env_data_2019.json'

    extract_env_data(dict2007, output2007)
    extract_env_data(dict2019, output2019)
