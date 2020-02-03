import json
import csv
from pathlib import Path


def convert_factbook_json_to_dict(path: Path):
    with open(path, 'r', encoding="utf8") as jsonfile:
        data = json.load(jsonfile)
    return data


def extract_env_data(full_data: dict):

    env_dict = {}

    for country_name, country in full_data['countries'].items():
        country_dict = {}
        env_issues = []

        try:
            env_issues = country['data']['geography']['environment']['current_issues']
            country_name = country['data']['name']
        except KeyError:
            print(f"Key does not exist for country {country_name}")

        country_dict["environmental_issues"] = env_issues
        env_dict[country_name] = country_dict

    return env_dict

def get_country_list(full_data: dict, outpath):
    country_list = []
    for country_name in full_data:
        try:
            country_name = country_name
        except KeyError:
            print(f"Key does not exist for country {country_name}")

        country_list.append(country_name)

    with open(outpath, 'w+') as file:
        file.write("Counties\n")
        for listitem in country_list:
            file.write('%s\n' % listitem)
    
    return country_list

def get_subtractions_additions(env_dict1, env_dict2):
    add_dict = {}
    sub_dict = {}
    for key in env_dict1:
        try:
            add_dict[key] = set(env_dict2[key]['environmental_issues']) - set(env_dict1[key]['environmental_issues'])
            sub_dict[key] = set(env_dict1[key]['environmental_issues']) - set(env_dict2[key]['environmental_issues'])
        except KeyError:
            print("Key does not exist")

    print(add_dict['China'])
    print(sub_dict['China'])

    with open(output_path, 'w+', newline='') as outfile:
        w = csv.DictWriter(outfile, ['country', 'environmental_issue'])
        w.writeheader()
        for key, values in country_dict.items():
            for value in values['environmental_issues']:
                w.writerow({'country' : key, 'environmental_issue': value})


def dict_to_csv_tableau(country_dict, output_path):
    
    with open(output_path, 'w+', newline='') as outfile:
        w = csv.DictWriter(outfile, ['country', 'environmental_issue'])
        w.writeheader()
        for key, values in country_dict.items():
            for value in values['environmental_issues']:
                w.writerow({'country' : key, 'environmental_issue': value})


if __name__ == "__main__":
    parent_raw = Path(__file__).parent.parent.parent / 'data' / 'raw'
    parent_processed = Path(__file__).parent.parent.parent / 'data' / 'processed'

    data2007 = parent_raw / 'weekly_json' / '2007-06-18_factbook.json'
    data2019 = parent_raw / 'factbook.json'

    dict2007 = convert_factbook_json_to_dict(data2007)
    dict2019 = convert_factbook_json_to_dict(data2019)

    output2007 = parent_processed / 'env_data_2007.csv'
    output2019 = parent_processed / 'env_data_2019.csv'
    country_list = parent_processed / 'clist.txt'

    env_dict2007 = extract_env_data(dict2007)
    env_dict2019 = extract_env_data(dict2019)

    dict_to_csv_tableau(env_dict2007, output2007)
    dict_to_csv_tableau(env_dict2019, output2019)

    get_country_list(env_dict2019, country_list)

    get_subtractions_additions(env_dict2007, env_dict2019)