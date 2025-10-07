#!/usr/bin/env python3
import yaml
import subprocess
import sys
import os
from pathlib import Path

def load_yaml_config(config_file):
    """Load and parse the YAML configuration file."""
    try:
        with open(config_file, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Error: Configuration file '{config_file}' not found.")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        sys.exit(1)

def run_command(command):
    """Run a shell command and print output."""
    print(f"\nRunning: {' '.join(command)}")
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n Error running command: {' '.join(command)}")
        print(e.stderr)
        return False

def init_backend(config):
    backend = config.get('backend', {})
    project = config['project_name']
    env = config['environment']
    
    state_key = f"projects/{project}/{env}/terraform.tfstate"

    backend_config = [
        f"-backend-config=bucket={backend['bucket']}",
        f"-backend-config=key={state_key}",
        f"-backend-config=region={backend['region']}",
       # f"-backend-config=dynamodb_table={backend['dynamodb_table']}",
        "-reconfigure"
    ]
    
    print("\n🔄 Initializing Terraform backend...")
    if not run_command(['terraform', 'init'] + backend_config):
        sys.exit(1)
    print(" Terraform backend initialized successfully.")

def main():
    print("\n" + "="*60)
    print("  QUICK DESTROY - AutoAWS Infrastructure")
    print("="*60 + "\n")

    if len(sys.argv) != 2:
        print("Usage: python destroy.py <config_file.yaml>")
        sys.exit(1)

    config_file = sys.argv[1]
    config = load_yaml_config(config_file)

    project = config['project_name']
    env = config['environment']

    print(f" Project: {project}")
    print(f" Environment: {env}\n")

    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    os.chdir(project_root)
    
    # Step 1: Initialize backend
    init_backend(config)

    # Step 2: Confirm destroy
    print("⚠️ WARNING: This will permanently destroy all infrastructure for this project!")
    response = input("Type 'yes' to continue: ")
    if response.lower() != 'yes':
        print("Destroy cancelled.")
        sys.exit(0)

    # Step 3: Run destroy
    print("\n Destroying infrastructure...")
    if not run_command(['terraform', 'destroy', '-auto-approve']):
        print("\n Destroy failed.")
        sys.exit(1)

    print(f"\n Infrastructure for {project}-{env} destroyed successfully!")

    # Step 4: Cleanup option
    cleanup = input("\n Remove Terraform local files (terraform.tfvars, .terraform)? (yes/no): ")
    if cleanup.lower() == 'yes':
        print("\nCleaning up local Terraform files...")
        files = ['terraform.tfvars', '.terraform.lock.hcl']
        for f in files:
            if os.path.exists(f):
                os.remove(f)
                print(f"Removed {f}")
        if os.path.exists('.terraform'):
            import shutil
            shutil.rmtree('.terraform')
            print("Removed .terraform directory")
        print(" Cleanup complete.")
    
    print("\nAll done!")

if __name__ == "__main__":
    main()