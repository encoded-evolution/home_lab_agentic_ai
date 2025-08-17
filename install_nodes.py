import os
import subprocess
import shutil
import time
import argparse
import platform
import sys


def run_command(cmd, cwd=None):
    """Run a shell command and print it."""
    print("Running:", " ".join(cmd))
    return subprocess.run(cmd, cwd=cwd, check=True)
    
    
"""Install n8n community nodes"""
print("Installing n8n community nodes...")
cmd = ["docker", "exec", "-it", "n8n", "sh", "-c", "cd ~/.n8n/nodes; npm i n8n-nodes-lightrag; npm i n8n-nodes-query-retriever-rerank; exit"]
run_command(cmd)