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


def create_tfvars(config):
    """Create a terraform.tfvars file from YAML config"""
    tfvars_content = []

    # Basuc variables
    
    tfvars_content.append(f'project_name = "{config["project_name"]}"')
    tfvars_content.append(f'environment = "{config["environment"]}"')
    tfvars_content.append(f'aws_region = "{config["aws_region"]}"')
   
    # Common tags
    if 'common_tags' in config:
        tags_str = json.dumps(config['common_tags'])
        tfvars_content.append(f'common_tags = {tags_str}')
    
    # Module controls
    tfvars_content.append(f'enable_vpc = {str(config.get("enable_vpc", False)).lower()}')
    
    # VPC Configuration
    if 'vpc_cidr' in config:
        tfvars_content.append(f'vpc_cidr = "{config["vpc_cidr"]}"')
    
    tfvars_content.append(f'enable_dns_hostnames = {str(config.get("enable_dns_hostnames", True)).lower()}')
    tfvars_content.append(f'enable_dns_support = {str(config.get("enable_dns_support", True)).lower()}')
    
    # Subnets
    if 'public_subnets' in config:
        public_subnets = json.dumps(config['public_subnets'], indent=2)
        tfvars_content.append(f'public_subnets = {public_subnets}')
    
    if 'private_subnets' in config:
        private_subnets = json.dumps(config['private_subnets'], indent=2)
        tfvars_content.append(f'private_subnets = {private_subnets}')
    
    # Services (if present)
    if "services" in config:
        services_str = json.dumps(config["services"], indent=2)
        tfvars_content.append(f'services = {services_str}')
    
    # Write to file
    with open('terraform.tfvars', 'w') as f:
        f.write('\n'.join(tfvars_content))
    
    print("Created terraform.tfvars")
    
