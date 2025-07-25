# 🛠️ Базовая настройка SSH внутри Docker-контейнера

## 1. Создаем Docker-контейнер с SSH-сервером

```bash
sudo docker run -d -p 2222:22 rastasheep/ubuntu-sshd
```

## 2. Генерируем SSH-ключи (если ещё не созданы)

```bash
ssh-keygen
```

## 3. Просматриваем публичный ключ

```bash
cat ~/.ssh/id_rsa.pub
```

## 4. Подключаемся к контейнеру от имени `root`

```bash
ssh -p 2222 root@localhost
```

> 📝 Пароль по умолчанию у `rastasheep/ubuntu-sshd` — `root`

## 5. Обновляем пакеты и устанавливаем `nano`

```bash
apt update
apt install nano
```

## 6. Создаем нового пользователя `dev` и задаем пароль

```bash
useradd -m dev
passwd dev
```

## 7. Создаем каталог `.ssh` и файл `authorized_keys`

```bash
mkdir /home/dev/.ssh
nano /home/dev/.ssh/authorized_keys
```

> Вставьте публичный ключ из пункта 3 в файл `authorized_keys`

## 8. Настраиваем права доступа

```bash
chown -R dev:dev /home/dev/.ssh
chmod 700 /home/dev/.ssh
chmod 600 /home/dev/.ssh/authorized_keys
```

## 9. Настраиваем `sshd_config`

```bash
nano /etc/ssh/sshd_config
```

Измените или раскомментируйте следующие строки:

```
PermitRootLogin no
PubkeyAuthentication yes
PasswordAuthentication no
```

## 10. Перезапускаем SSH-сервер

```bash
service ssh restart
```

## 11. Подключаемся к контейнеру под пользователем `dev`

```bash
ssh -p 2222 dev@localhost
```

---

✅ **Готово! Базовая настройка SSH завершена.**
