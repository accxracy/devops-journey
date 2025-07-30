#!/usr/bin/env python3

import os
import subprocess
from index import html_content

def run(command, check=True):
    try:
        subprocess.run(command, check=check, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {command}")
        print(f"Error code: {e.returncode}")
        exit(1)

def write(path, content):
    with open(path, 'w') as fin:
        fin.write(content)

def main():
    if not os.getuid():
        print("Start")

        print("Updating packages...")
        run("apt update")

        print("Installing nginx...")
        run("apt install -y nginx")

        write("/var/www/html/index.nginx-debian.html", html_content)

        print("Restart services...")
        run("systemctl restart nginx")
        run("systemctl enable nginx")

        print("Done")
        return 0
    else:
        print("Please run as superuser")
        return 1

if __name__ == "__main__":
    main()
