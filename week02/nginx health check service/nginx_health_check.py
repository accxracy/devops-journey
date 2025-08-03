#!/usr/bin/env python3

import requests
from datetime import datetime

URL_CHECK = "http://localhost"
LOG_PATH = "/var/log/nginx_h/nginx_health.log"

def make_log(log_message):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as fin:
            fin.write(f"{time} : {log_message}\n")
    except Exception as e:
        print(f"Не удалось записать лог: {e}")

def main():
    try:
        response = requests.get(URL_CHECK, timeout=5)
        if response.status_code == 200:
            make_log(f"OK : {response.status_code}")
        else:
            make_log(f"FAIL : {response.status_code}")
    except requests.exceptions.RequestException as ex:
        make_log(f"ERROR : {ex}")

if __name__ == "__main__":
    main()
