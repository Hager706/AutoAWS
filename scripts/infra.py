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
    
def run_terraform_commands(command):
    """Run terraform command and handle output"""
    print(f"Running: terraform {' '.join(command)}")
    try:
        result = subprocess.run(['terraform'] + command, 
                                capture_output=True, text=True, check=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running terraform {' '.join(command)}:")
        print(e.stderr)
        return False
    
def main():
    if len(sys.argv) < 3:
        print("Usage: infra.py <config.yaml> <deploy|destroy>")
        sys.exit(1)
    config_file = sys.argv[1]
    action = sys.argv[2].lower()

    print(f"Starting AWS infrastructure ({action})...")
    print(f"Loading configuration from: {config_file}")

    # Load configuration
    config = load_config(config_file)

    # Change to project root directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    os.chdir(project_root)

    # Create terraform.tfvars
    create_tfvars(config)


    print("Initializing Terraform...")
    if not run_terraform_commands(['init']):
        sys.exit(1)
    

    # Plan
    if action == 'deploy':
        print("Creating execution plan...")
        if not run_terraform_commands(['plan']):
            sys.exit(1)
    elif action == 'destroy':
        print("Creating destroy plan...")
        if not run_terraform_commands(['plan', '-destroy']):
            sys.exit(1)


    # # Ask for confirmation 
    # response = input(f"Do you want to {action} these changes? (yes/no):")
    # if response.lower() != 'yes':
    #     print("Operation cancelled")
    #     sys.exit(0)
    
    # Apply or Destroy
    if action == 'deploy':
        print("Applying changes...")
        if run_terraform_commands(['apply', '-auto-approve']):
            print("Infrastructure deployed successfully.")
        else:
            print("Deploying failed.")
            sys.exit(1)
    elif action == 'destroy':
        print("Destroying infrastructure...")
        if run_terraform_commands(['destroy', '-auto-approve']):
            print("Infrastructure destroyed successfully.")
        else:
            print("Destroying failed.")
            sys.exit(1)
    else:
        print("Invalid action. Use 'deploy' or 'destroy'.")
        sys.exit(1)

if __name__ == "__main__":
    main()
