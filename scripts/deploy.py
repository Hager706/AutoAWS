#!/usr/bin/env python3
import yaml
import subprocess
import sys
import os
import json
from pathlib import Path

def load_yaml_config(config_file):
    try:
        with open(config_file, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Error: Configuration file '{config_file}' not found")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        sys.exit(1)

def init_backend(config):
    
    backend = config.get('backend', {})
    project = config['project_name']
    env = config['environment']
    
    state_key = f"projects/{project}/{env}/terraform.tfstate"

    backend_config = [
        f"-backend-config=bucket={backend['bucket']}",
        f"-backend-config=key={state_key}",
        f"-backend-config=region={backend['region']}",
        #f"-backend-config=dynamodb_table={backend['dynamodb_table']}",
        "-reconfigure"  # Allow switching between backends
    ]
    
    print("\n🔄 Initializing Terraform...")
    result = subprocess.run(
        ['terraform', 'init'] + backend_config,
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"Terraform init failed:")
        print(result.stderr)
        sys.exit(1)
    
    print("Terraform initialized successfully!")
    print(result.stdout)

def create_tfvars(config):
    tfvars_content = []
    
    tfvars_content.append(f'project_name = "{config["project_name"]}"')
    tfvars_content.append(f'environment = "{config["environment"]}"')
    tfvars_content.append(f'aws_region = "{config["aws_region"]}"')
    
    if 'common_tags' in config:
        tags_str = json.dumps(config['common_tags'])
        tfvars_content.append(f'common_tags = {tags_str}')
    
    tfvars_content.append(f'enable_vpc = {str(config.get("enable_vpc", False)).lower()}')
    
    if 'vpc_cidr' in config:
        tfvars_content.append(f'vpc_cidr = "{config["vpc_cidr"]}"')
    
    tfvars_content.append(f'enable_dns_hostnames = {str(config.get("enable_dns_hostnames", True)).lower()}')
    tfvars_content.append(f'enable_dns_support = {str(config.get("enable_dns_support", True)).lower()}')
    
    if 'public_subnets' in config:
        public_subnets = json.dumps(config['public_subnets'], indent=2)
        tfvars_content.append(f'public_subnets = {public_subnets}')
    
    if 'private_subnets' in config:
        private_subnets = json.dumps(config['private_subnets'], indent=2)
        tfvars_content.append(f'private_subnets = {private_subnets}')
    
    if "services" in config:
        services_str = json.dumps(config["services"], indent=2)
        tfvars_content.append(f'services = {services_str}')
    
    with open('terraform.tfvars', 'w') as f:
        f.write('\n'.join(tfvars_content))
    
    print("Created terraform.tfvars")

def run_terraform_command(command):
    print(f"\n Running: terraform {' '.join(command)}")
    try:
        result = subprocess.run(
            ['terraform'] + command,
            capture_output=True,
            text=True,
            check=True
        )
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running terraform {' '.join(command)}:")
        print(e.stderr)
        return False

def main():
    if len(sys.argv) != 2:
        print("Usage: python deploy.py <config_file.yaml>")
        sys.exit(1)
    
    config_file = sys.argv[1]
    print(f"Loading configuration from: {config_file}")
    
    config = load_yaml_config(config_file)
    
    project = config['project_name']
    env = config['environment']
    
    print(f"\nProject: {project}")
    print(f"🌍 Environment: {env}")
    
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    os.chdir(project_root)
    
    init_backend(config)
    
    create_tfvars(config)
    
    if not run_terraform_command(['plan', '-out=tfplan']):
        sys.exit(1)
    
    response = input(f"\n Deploy {project}-{env}? (yes/no): ")
    if response.lower() != 'yes':
        print(" Deployment cancelled")
        sys.exit(0)
    
    # Apply
    print(f"\n Deploying {project}-{env}...")
    if run_terraform_command(['apply', 'tfplan']):
        print(f"\n {project}-{env} deployed successfully!")
    else:
        print("\n Deployment failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()