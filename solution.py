import json
from datetime import datetime


def sanitize_key(key):
    return key.strip()


def sanitize_string(value):
    if value is None:
        return None
    return value.strip()


def transform_number(value):
    if value is None:
        return None
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return None


def transform_bool(value):
    if value is None:
        return None
    value = value.strip().lower()
    if value in ['1', 't', 'true']:
        return True
    elif value in ['0', 'f', 'false']:
        return False
    else:
        return None


def transform_null(value):
    if value is None:
        return None
    value = value.strip().lower()
    if value in ['1', 't', 'true']:
        return None
    elif value in ['0', 'f', 'false']:
        return False
    else:
        return None


def transform_string(value):
    if value is None:
        return None
    value = value.strip()
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            try:
                return int(datetime.fromisoformat(value).timestamp())
            except ValueError:
                return value


def transform_value(value):
    if isinstance(value, dict):
        if 'S' in value:
            return transform_string(value['S'])
        elif 'N' in value:
            return transform_number(value['N'])
        elif 'BOOL' in value:
            return transform_bool(value['BOOL'])
        elif 'NULL' in value:
            return transform_null(value['NULL'])
        else:
            return transform_dict(value)
    elif isinstance(value, list):
        return [transform_value(v) for v in value]
    else:
        return value


def transform_dict(d):
    transformed = {}
    for key, value in d.items():
        key = sanitize_key(key)
        if key and value:
            transformed[key] = transform_value(value)
    return transformed


def transform_json(json_str):
    data = json.loads(json_str)
    return [transform_dict(data)]
json_str = '{"number_1": {"N": "1.50"},"string_1": {"S": "784498 "},"string_2": {"S": "2014-07-16T20:55:46Z"},"map_1": {"M": {"bool_1": {"BOOL": "truthy"},"null_1": {"NULL ": "true"},"list_1": {"L": [{"S": ""},{"N": "011"},{"N": "5215s"},{"BOOL": "f"},{"NULL": "0"}]}}},"list_2": {"L": "noop"},"list_3": {"L": ["noop"]},"": {"S": "noop"}}'
transformed_json = transform_json(json_str)
print(json.dumps(transformed_json, indent=2))