
# Nginx Health Check with systemd Timer

Это пример настройки периодической проверки доступности Nginx-сервера с использованием Python-скрипта и systemd-сервиса с таймером.

---

## 🔧 Содержание

1. [Python-скрипт для проверки](#-python-скрипт-для-проверки)
2. [Настройка systemd-сервиса](#-настройка-systemd-сервиса)
3. [Создание таймера systemd](#-создание-таймера-systemd)
4. [Запуск и проверка работы](#-запуск-и-проверка-работы)

---

## 🐍 Python-скрипт для проверки

```python
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
```

Убедитесь, что скрипт имеет права на исполнение:

```bash
chmod +x /путь/до/скрипта.py
```

---

## 🛠 Настройка systemd-сервиса

Создайте файл `/etc/systemd/system/nginx_health_check.service` со следующим содержимым:

```ini
[Unit]
Description=Checking nginx 

[Service]
Type=oneshot
ExecStart=/usr/bin/python3 /путь/до/скрипта.py
```

---

## ⏲ Создание таймера systemd

Создайте файл `/etc/systemd/system/nginx_health_check.timer`:

```ini
[Unit]
Description=Run nginx check every 5sec

[Timer]
OnBootSec=10s
OnUnitActiveSec=5s
Persistent=false

[Install]
WantedBy=timer.target
```

---

## 🚀 Запуск и проверка работы

Перезагрузите systemd-демон:

```bash
sudo systemctl daemon-reload
```

Активируйте и запустите таймер:

```bash
sudo systemctl enable nginx_health_check.timer
sudo systemctl start nginx_health_check.timer
```

---

## 🔍 Проверка

Посмотреть логи сервиса:

```bash
journalctl -u nginx_health_check.service
```

Проверить статус:

```bash
systemctl status nginx_health_check.service
```

Просмотреть лог-файл:

```bash
cat /var/log/nginx_h/nginx_health.log
```

---

## ✅ Готово!
Теперь вы можете быть уверены, что ваш nginx регулярно проверяется!
