# 🛡 Права и пользователи в Linux с использованием ACL

В этом руководстве мы рассмотрим, как настроить права доступа для различных групп пользователей в Linux с использованием механизма **ACL (Access Control Lists)**.

## Зачем это нужно?

Представьте себе ситуацию: у вас есть проектная директория, к которой должны иметь доступ разные группы пользователей с разными правами:

- **developers** — полный доступ (`rwx`, права `7`)
- **testers** — только чтение и выполнение (`r-x`, права `5`)
- Остальные — **никакого доступа**

Чтобы реализовать такое разграничение прав, мы воспользуемся **ACL**, который расширяет стандартную модель прав доступа в Linux.

> ⚠️ Обратите внимание: для использования ACL файловая система (например, `ext4`) должна поддерживать расширенные атрибуты.

---

## 🔧 Шаги по настройке

### 1. Установка необходимых пакетов

```bash
sudo apt update && sudo apt install nano acl
```

---

### 2. Создание групп

```bash
groupadd developers
groupadd testers
```

---

### 3. Создание пользователей и добавление их в группы

```bash
useradd -g developers -m developer1
useradd -g developers -m developer2

useradd -g testers -m tester1
useradd -g testers -m tester2
```

---

### 4. Создание директории проекта

```bash
mkdir -p /srv/project
```

---

### 5. Установка базовых прав на директорию

```bash
chmod 770 /srv/project
```

---

### 6. Назначение владельца и группы

```bash
chown root:developers /srv/project
```

---

### 7. Установка SGID для наследования группы

```bash
chmod g+s /srv/project
```

---

### 8. Назначение прав ACL для группы `testers`

```bash
setfacl -m g:testers:rx /srv/project
```

---

### 9. Установка **наследуемых** ACL (по умолчанию для новых файлов)

```bash
setfacl -d -m g:developers:rwx /srv/project
setfacl -d -m g:testers:rx /srv/project
setfacl -d -m o:--- /srv/project
```

---

### 10. Проверка доступа

#### ✅ Developer создает файл

```bash
sudo -u developer1 touch /srv/project/dev.txt
ls /srv/project
# Ожидаемый результат: dev.txt
```

#### ❌ Tester пробует создать файл

```bash
sudo -u tester1 touch /srv/project/test.txt
# Ожидаемый результат: Permission denied
```

---

### 11. Проверка ACL

```bash
getfacl /srv/project
```

#### Пример вывода:

```
# file: srv/project/
# owner: root
# group: developers
# flags: -s-
user::rwx
group::rwx
group:testers:r-x
mask::rwx
other::---
default:user::rwx
default:group::rwx
default:group:developers:rwx
default:group:testers:r-x
default:mask::rwx
default:other::---
```

---

## 📌 Заключение

С помощью ACL вы можете гибко управлять правами доступа в Linux на уровне файлов и каталогов. Это особенно удобно в многопользовательской среде, где необходимо разграничить доступ без создания сложных структур директорий.

---

## 📁 Полезные команды

| Команда                | Назначение                                      |
|------------------------|-------------------------------------------------|
| `setfacl`              | Установка/изменение ACL                         |
| `getfacl`              | Просмотр текущих ACL                            |
| `chmod g+s`            | Установка SGID для наследования группы         |
| `chown`                | Смена владельца и группы                        |

---

**💡 Подходит для систем с поддержкой ACL (например, ext4)**
