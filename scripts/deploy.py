#!/usr/bin/env python3
import yaml
import subprocess
import sys
import os
import json
from pathlib import Path

def load_yaml_config(config_file):
    """Load and parse YAML configuration file"""
    try:
        with open(config_file, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f" Error: Configuration file '{config_file}' not found")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f" Error parsing YAML file: {e}")
        sys.exit(1)

def create_tfvars(config):
    """Create terraform.tfvars file from YAML config"""
    tfvars_content = []
    
    # Basic variables
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
    
    # Write to file
    with open('terraform.tfvars', 'w') as f:
        f.write('\n'.join(tfvars_content))
    
    print(" Created terraform.tfvars")

def run_terraform_command(command):
    """Run terraform command and handle output"""
    print(f" Running: terraform {' '.join(command)}")
    try:
        result = subprocess.run(['terraform'] + command, 
                              capture_output=True, text=True, check=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f" Error running terraform {' '.join(command)}:")
        print(e.stderr)
        return False

def main():
    if len(sys.argv) != 2:
        print("Usage: python deploy.py <config_file.yaml>")
        sys.exit(1)
    
    config_file = sys.argv[1]
    print(f" Starting AWS VPC deployment...")
    print(f" Loading configuration from: {config_file}")
    
    # Load configuration
    config = load_yaml_config(config_file)
    
    # Change to project root directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    os.chdir(project_root)
    
    # Create tfvars file
    create_tfvars(config)
    
    # Initialize Terraform
    print("\n Initializing Terraform...")
    if not run_terraform_command(['init']):
        sys.exit(1)
    
    # Plan
    print("\n Creating execution plan...")
    if not run_terraform_command(['plan']):
        sys.exit(1)
    
    # Ask for confirmation
    response = input("\n Do you want to apply these changes? (yes/no): ")
    if response.lower() != 'yes':
        print(" Deployment cancelled")
        sys.exit(0)
    
    # Apply
    print("\n Applying changes...")
    if run_terraform_command(['apply', '-auto-approve']):
        print("\n VPC Infrastructure deployed successfully!")
        print("🎉 Your AWS VPC and subnets are ready!")
    else:
        print("\n Deployment failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()