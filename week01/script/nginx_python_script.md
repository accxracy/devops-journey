
# 🛠️ Установка Nginx с помощью Python-скрипта (Debian-based)

Автоматизация базовой установки и настройки **nginx** на Debian-подобных системах с помощью Python-скрипта.

## 📂 Структура проекта

```
App/
├── index.py         # Содержит HTML-контент
└── script.py        # Основной скрипт установки nginx
```

---

## 📄 1. `index.py` — HTML для проверки nginx

Создайте файл `index.py` с HTML-контентом:

```python
html_content = """<html>
    <head><title>nginx</title></head>
    <body>
        <h1> nginx </h1>
    </body>
</html>"""
```

---

## ⚙️ 2. `script.py` — Скрипт установки

Создайте файл `script.py` и добавьте в него:

```python
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
```

---

## 🚀 3. Запуск на целевой машине

### 1. 📤 Отправьте файлы `index.py` и `script.py` на целевую машину:

### 2. 📁 Перейдите в каталог со скриптами:
```bash
cd /путь/к/скрипту/
```

### 3. 🧾 Сделайте `script.py` исполняемым:
```bash
chmod +x script.py
```

### 4. 🧑‍💻 Запустите скрипт от суперпользователя:
```bash
sudo ./script.py
```

---

## 🌐 4. Проверка работы

Откройте в браузере:

```
http://localhost
```

Вы должны увидеть страницу с заголовком:

```html
<h1> nginx </h1>
```

---

✅ Готово! 
