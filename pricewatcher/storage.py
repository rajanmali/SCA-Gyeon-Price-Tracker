import os
import json
import yaml
from pricewatcher.config import PRODUCTS_YAML, PRICES_JSON  # import paths from config


def read_yaml(file_path=PRODUCTS_YAML):
    """Read a YAML file and return its contents."""
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)


def write_json(file_path=PRICES_JSON, data=None):
    """Write data to a JSON file."""
    if data is None:
        data = {}
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)


def read_json(file_path=PRICES_JSON) -> dict:
    """Read JSON file and return dictionary. Returns empty dict if file is empty or missing."""
    if not os.path.exists(file_path) or os.stat(file_path).st_size == 0:
        return {}
    with open(file_path, "r") as f:
        return json.load(f)
