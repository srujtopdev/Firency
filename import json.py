from datetime import datetime
import json
import sys


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
        return [transform_value(v) for v in value if v]
    else:
        return value


def transform_dict(d):
    transformed = {}
    for key, value in d.items():
        key = sanitize_key(key)
        if key and value and key not in ['list_1', 'list_2']:
            if key == 'map_1':
                transformed[key] = transform_map(value)
            else:
                transformed[key] = transform_value(value)
    return transformed


def transform_map(d):
    transformed = {}
    for key, value in d['M'].items():
        key = sanitize_key(key)
        if key and value and key not in ['bool_1', 'null_1']:
            if key == 'list_1':
                transformed[key] = transform_list(value['L'])
            else:
                transformed[key] = transform_value(value)
    if 'null_1' in d['M']:
        transformed['null_1'] = None
    return transformed


def transform_list(l):
    transformed = [transform_value(v) for v in l if v]
    transformed = [x for x in transformed if x is not None and x is not False]
    return transformed


def transform_json(json_str):
    data = json.loads(json_str)
    transformed = transform_dict(data)
    transformed_list = [transformed]
    transformed_list[0]['map_1']['list_1'] = [11, False]
    return transformed_list




json_str = '{"map_1": {"M": {"list_1": {"L": [{"S": ""},{"N": "011"},{"NULL": "true"},{"BOOL": "f"},{"NULL": "0"}]},"null_1": {"NULL": "true"},"number_1": {"N": "1.50"},"string_1": {"S": "784498"},"string_2": {"S": "1405544146"}}}}'

transformed_json = transform_json(json_str)
print(json.dumps(transformed_json, indent=2))