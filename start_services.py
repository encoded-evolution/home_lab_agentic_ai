#!/usr/bin/env python3
"""
start_services.py

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


def run_install_workflows(script_path):
    script_command = f'python {script_path}'
    process = subprocess.Popen(script_command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    if error:
        print(f"Error occurred: {error.decode()}")
    else:
        print("Script executed successfully.")

def run_command(cmd, cwd=None):
    """Run a shell command and print it."""
    print("Running:", " ".join(cmd))
    return subprocess.run(cmd, cwd=cwd, check=True)

def prepare_main_env():
    """Copy .env.home_ai to .env in main folder"""
    env_target_path = os.path.join(".env")
    env_source_path = os.path.join(".env.home_ai")
    print("Copying .env.home_ai in root to .env in root...")
    shutil.copyfile(env_example_path, env_target_path)
    
def clone_crawl4ai_repo():
    """Clone the crawl4ai repository using sparse checkout if not already present."""
    if not os.path.exists("crawl4ai"):
        print("Cloning the crawl4ai repository...")
        run_command([
            "git", "clone", 
            "https://github.com/unclecode/crawl4ai"
        ])
    else:
        print("crawl4ai repository already exists, updating...")
        os.chdir("crawl4ai")
        run_command(["git", "pull"])
        os.chdir("..")

def prepare_crawl4ai_env():
    """Copy .env to .llm.env in crawl4ai"""
    env_path = os.path.join("crawl4ai", ".llm.env")
    env_example_path = os.path.join(".env")
    print("Copying .env in root to .env in crawl4ai...")
    shutil.copyfile(env_example_path, env_path)

def clone_lightrag_repo():
    """Clone the crawl4ai repository using sparse checkout if not already present."""
    if not os.path.exists("LightRAG"):
        print("Cloning the LightRAG repository...")
        run_command([
            "git", "clone", 
            "https://github.com/HKUDS/LightRAG.git"
        ])
    else:
        print("LightRAG repository already exists, updating...")
        os.chdir("LightRAG")
        run_command(["git", "pull"])
        os.chdir("..")

def prepare_lightrag_env():
    """Copy .env to .env in LightRAG"""
    env_path = os.path.join("LightRAG", ".env")
    env_example_path = os.path.join(".env")
    print("Copying .env in root to .env in LightRAG...")
    shutil.copyfile(env_example_path, env_path)
    
def prepare_postgres_storage_point():
    path = "./postgres_storage/data"
    if not os.path.exists(path):
        # Create the new directory
        os.makedirs(path)
        print("Created {path}")
    else:
        print("Path {path} already exists")

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

def start_crawl4ai(environment=None):
    """Start the crawl4ai services (using its compose file)."""
    print("Starting crawl4ai services...")
    try:
        cmd = ["docker", "compose", "-p", docker_container_name, "-f", "crawl4ai/docker-compose.yml"]
        if environment and environment == "public":
            cmd.extend(["-f", "docker-compose.override.public.crawl4ai.yml"])
        cmd.extend(["up", "-d"])
        run_command(cmd)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        print(f"Wait until all software is downloaded, and running.  Then restart the docker containers")
        print(f"Wait until all software is downloaded, and running.  Then restart the docker containers")

def start_lightrag(environment=None):
    """Start the LightRAG services (using its compose file)."""
    print("Starting LightRAG services...")
    cmd = ["docker", "compose", "-p", docker_container_name, "-f", "LightRAG/docker-compose.yml"]
    if environment and environment == "public":
        cmd.extend(["-f", "docker-compose.override.public.LightRAG.yml"])
    cmd.extend(["up", "-d"])
    run_command(cmd)

def install_n8n_nodes(profile=None, environment=None):
    """Install n8n community nodes"""
    print("Installing n8n community nodes...")
    cmd = ["docker", "exec", "-it", "n8n", "sh", "-c", "'cd ~/.n8n/nodes; npm install n8n-nodes-lightrag; npm install n8n-nodes-query-retriever-rerank; exit'"]
    run_command(cmd)
    
def get_selenium_build_components(profile=None, environment=None):
    """Get the extra build components for Selenium"""
    print("Installing build components for Selenium...")
    cmd = ["curl", "-o", "chrome-cleanup.conf", "https://github.com/SeleniumHQ/docker-selenium/blob/trunk/NodeChromium/chrome-cleanup.conf"]
    run_command(cmd)
    cmd = ["curl", "-o", "chrome-cleanup.sh", "https://github.com/SeleniumHQ/docker-selenium/blob/trunk/NodeChromium/chrome-cleanup.sh"]
    run_command(cmd)
    cmd = ["curl", "-o", "wrap_chromium_binary", "https://github.com/SeleniumHQ/docker-selenium/blob/trunk/NodeChromium/wrap_chromium_binary"]
    run_command(cmd)

def start_selenium(profile=None, environment=None):
    """Starting Selenium"""
    print("Starting Selenium...")
    try:
        cmd = ["docker", "run", "--name", "selenium_chrome", "-d", "-p", "4444:4444", "selenium/standalone-chrome"]
        run_command(cmd)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    

def start_local_ai(profile=None, environment=None):
    """Start the Basic AI services (using its compose file)."""
    print("Starting Basic AI services...")
    cmd = ["docker", "compose", "-p", docker_container_name]
    if profile and profile != "none":
        cmd.extend(["--profile", profile])
    cmd.extend(["-f", "docker-compose.yml"])
    # if environment and environment == "private":
        # cmd.extend(["-f", "docker-compose.override.private.yml"])
    # if environment and environment == "public":
        # cmd.extend(["-f", "docker-compose.override.public.yml"])
    cmd.extend(["up", "-d"])
    run_command(cmd)
    

def main():
    parser = argparse.ArgumentParser(description='Start the local AI and Supabase services.')
    parser.add_argument('--profile', choices=['cpu', 'gpu-nvidia', 'gpu-amd', 'none'], default='cpu',
                      help='Profile to use for Docker Compose (default: cpu)')
    parser.add_argument('--environment', choices=['private', 'public'], default='private',
                      help='Environment to use for Docker Compose (default: private)')
    args = parser.parse_args()

    stop_existing_containers(args.profile)

    prepare_main_env()
    
    clone_lightrag_repo()
    time.sleep(4)
    prepare_lightrag_env()
    clone_crawl4ai_repo()
    prepare_crawl4ai_env()

    get_selenium_build_components()
    time.sleep(4)
    
    run_install_workflows('install_workflows.py')
    time.sleep(1)

    # Then start the local AI services
    start_local_ai(args.profile, args.environment)
    # install_n8n_nodes()
    # time.sleep(10)
    
    # Start Crawl4ai 
    start_crawl4ai(args.environment)
    # Give crawl4ai some time to initialize
    print("Waiting for crawl4ai to initialize...")
    time.sleep(1)
    
    start_selenium()


if __name__ == "__main__":
    main()
