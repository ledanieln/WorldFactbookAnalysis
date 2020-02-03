import pytest
from src.data.get_env_issues import convert_factbook_json_to_dict


@pytest.mark.unittest
def test_convert_to_json():
    data2007 = '../../data/raw/weekly_json/2007-06-18_factbook.json'
    data2019 = '../../data/raw/factbook.json'

    data2007 = convert_factbook_json_to_dict(data2007)
    data2019 = convert_factbook_json_to_dict(data2019)
    assert str(type(data2007)) == "<class \'dict\'>"
