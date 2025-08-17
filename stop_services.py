#!/usr/bin/env python3
"""
stop_services.py

This script starts the Supabase stack first, waits for it to initialize, and then starts
the local AI stack. Both stacks use the same Docker Compose project name ("localai")
so they appear together in Docker Desktop.
"""

import os
import subprocess
import shutil
import time
import argparse
import platform
import sys

docker_container_name = "agentic_home_ai_lab"

def run_command(cmd, cwd=None):
    """Run a shell command and print it."""
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, cwd=cwd, check=True)


def stop_existing_containers(profile=None):
    print("Stopping and removing existing containers for the unified project {docker_container_name}...")
    cmd = ["docker", "compose", "-p", docker_container_name]
    if profile and profile != "none":
        cmd.extend(["--profile", profile])
    cmd.extend(["-f", "docker-compose.yml", "down"])
    run_command(cmd)
    try:
        cmd = ["docker", "stop", "selenium_chrome"]
        response = run_command(cmd)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        pass
    try:
        cmd = ["docker", "rm", "selenium_chrome"]
        response = run_command(cmd)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        pass

def main():
    parser = argparse.ArgumentParser(description='Start the local AI and Supabase services.')
    parser.add_argument('--profile', choices=['cpu', 'gpu-nvidia', 'gpu-amd', 'none'], default='cpu',
                      help='Profile to use for Docker Compose (default: cpu)')
    parser.add_argument('--environment', choices=['private', 'public'], default='private',
                      help='Environment to use for Docker Compose (default: private)')
    args = parser.parse_args()

    stop_existing_containers(args.profile)

if __name__ == "__main__":
    main()
