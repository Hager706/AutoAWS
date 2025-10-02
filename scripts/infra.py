#!/usr/bin/env python3

import yaml
import subprocess
import os 
import sys
import json 
from pathlib import Path

def load_config(config_path):
    """Load and parse the YAML configuration file."""
    try:
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f" Error: Configuration file '{config_path}' not found.")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f" Error parsing YAML file: {e}")
        sys.exit(1)


