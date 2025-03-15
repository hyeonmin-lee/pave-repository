#!/usr/bin/env python3

import os
import sys
import subprocess
import requests
import hashlib
import tarfile
import json


def download_file(url, download_dir, filename):
    os.makedirs(download_dir, exist_ok=True)
    file_path = os.path.join(download_dir, filename)

    print(f"- Downloading {filename} from {url}")
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
    except Exception as e:
        print(e)
        input()
        return None

    print(f"- Downloaded to {file_path}")
    return file_path


def extract_file(file_path, extract_to, file_format):
    os.makedirs(extract_to, exist_ok=True)

    if file_format == "tar.xz":
        with tarfile.open(file_path, "r:xz") as tar:
            tar.extractall(path=extract_to)
    elif file_format == "tgz":
        with tarfile.open(file_path, "r:gz") as tar:
            tar.extractall(path=extract_to)
    elif file_format == "bz2":
        with tarfile.open(file_path, "r:bz2") as tar:
            tar.extractall(path=extract_to)
    else:
        print(f"Unsupported format: {file_format}")
        input()
        return False

    print(f"- Extracted to {extract_to}")
    return True


def process_entry(entry, download_dir):
    url = entry.get("url")
    if not url:
        print(f"\n[Warn] Skipping entry (empty URL)")
        return

    name = entry.get("name", "")
    file_format = entry.get("format", "").strip()
    install_path_list = entry.get("install_path", "./")
    download_path = entry.get("download_path", "").strip()
    
    if download_path != "":
        download_dir = download_path

    filename = name if name else url.split("/")[-1]

    print(f"\n## {filename}")
    file_path = download_file(url, download_dir, filename)
    
    if file_path == None:
        return

    if file_format in ["tar.xz", "tgz"]:
        for install_path in install_path_list:
            extract_file(file_path, install_path, file_format)

def main():
    download_dir = "downloaded/"
    os.makedirs(download_dir, exist_ok=True)

    with open("files.json", "r") as f:
        files = json.load(f)

    for entry in files:
        process_entry(entry, download_dir)

    print("\n[Done] All tasks completed.")


if __name__ == "__main__":
    main()


