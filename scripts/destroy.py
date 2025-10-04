#!/usr/bin/env python3

import subprocess
import sys
import os
from pathlib import Path

def run_command(command):
    print(f"Running: {' '.join(command)}")
    try:
        subprocess.run(command, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f" Error: {e}")
        return False

def main():
    print("\n" + "="*60)
    print("  QUICK DESTROY - AutoAWS Infrastructure")
    print("="*60 + "\n")
    
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    os.chdir(project_root)
    
    print(f"Working directory: {project_root}\n")
    
    # Warning
    print("WARNING: This will destroy ALL infrastructure!")
    print("This is a QUICK destroy with minimal checks.\n")
    
    response = input("Type 'yes' to continue: ")
    if response.lower() != 'yes':
        print("Cancelled")
        sys.exit(0)
    
    print("\n Initializing Terraform...")
    if not run_command(['terraform', 'init']):
        sys.exit(1)
    
    print("\n🔨 Destroying infrastructure...")
    if not run_command(['terraform', 'destroy', '-auto-approve']):
        print("\n Destroy failed!")
        sys.exit(1)
    
    print("\n Infrastructure destroyed successfully!")
    
    # Cleanup option
    cleanup = input("\n Remove Terraform files? (yes/no): ")
    if cleanup.lower() == 'yes':
        print("\n Cleaning up...")
        
        files = ['terraform.tfvars', '.terraform.lock.hcl']
        for f in files:
            if os.path.exists(f):
                os.remove(f)
                print(f" Removed {f}")
        
        if os.path.exists('.terraform'):
            import shutil
            shutil.rmtree('.terraform')
            print("Removed .terraform/")
    
    print("\n All done!\n")

if __name__ == "__main__":
    main()