import os
import json
import yaml


def read_yaml(file_path):
    """Read a YAML file and return its contents."""
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)


def write_json(file_path, data):
    """Write data to a JSON file."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)


def read_json(path: str) -> dict:
    """Read JSON file and return dictionary. Returns empty dict if file is empty or missing."""
    if not os.path.exists(path) or os.stat(path).st_size == 0:
        return {}
    with open(path, "r") as f:
        return json.load(f)
