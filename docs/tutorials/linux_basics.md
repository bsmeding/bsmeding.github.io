---
title: Basic Linux Commands for Development
tags:
    - linux
    - basics
    - tutorial
---
# Basic Linux Commands for Development

As a developer, understanding essential Linux commands is crucial. Whether you're managing files, setting up Python environments, or working with directories, these commands will help you get started.

---

## 📁 File and Directory Management

### List Files and Directories
List files in the current directory:
```bash
ls
```
Common options:
- `ls -l` : Long format listing
- `ls -a` : Show hidden files

### Create and Remove Directories
Create a new directory:
```bash
mkdir directory_name
```
Remove an empty directory:
```bash
rmdir directory_name
```
Remove a non-empty directory:
```bash
rm -r directory_name
```

### Navigate Between Directories
Change directory:
```bash
cd directory_name
```
Go up one level:
```bash
cd ..
```
Show current directory:
```bash
pwd
```

### Copy, Move, and Delete Files
Copy a file:
```bash
cp source destination
```
Copy a directory:
```bash
cp -r source_dir destination_dir
```
Move or rename a file or directory:
```bash
mv source destination
```
Delete a file:
```bash
rm file_name
```

---

## 🐍 Python and Pip Basics

### Check Python Version
```bash
python3 --version
```

### Install pip (Python Package Manager)
Debian/Ubuntu:
```bash
sudo apt install python3-pip
```
RedHat/CentOS:
```bash
sudo yum install python3-pip
```

### Manage Python Packages
Install a package:
```bash
pip install package_name
```
List installed packages:
```bash
pip list
```
Uninstall a package:
```bash
pip uninstall package_name
```

---

## 🏗️ Virtual Environments

Virtual environments isolate your project's dependencies from the global Python environment. This helps avoid conflicts and makes collaboration easier.

### Using venv (Python 3.3+)
Create a virtual environment:
```bash
python3 -m venv env
```
Activate it:
```bash
source env/bin/activate
```
Install dependencies:
```bash
pip install package_name
```
Deactivate when done:
```bash
deactivate
```

### Using virtualenv (Alternative)
Install virtualenv:
```bash
pip install virtualenv
```
Create a virtual environment:
```bash
virtualenv env_name
```
Activate:
```bash
source env_name/bin/activate
```
Deactivate:
```bash
deactivate
```

**Tip:** Use a `requirements.txt` file to share dependencies:
```bash
pip freeze > requirements.txt
pip install -r requirements.txt
```

[More on Python virtual environments](https://docs.python.org/3/tutorial/venv.html)

---

## 🔒 File Permissions and Ownership

### Change File Permissions
Make a file executable:
```bash
chmod +x script.sh
```
Set specific permissions:
```bash
chmod 644 file.txt
```

### Change File Ownership
Change owner and group:
```bash
sudo chown user:group file_name
```

---

## 📦 Package Management (Debian/Ubuntu)

Update package lists:
```bash
sudo apt update
```
Upgrade installed packages:
```bash
sudo apt upgrade
```
Install a package:
```bash
sudo apt install package_name
```
Remove a package:
```bash
sudo apt remove package_name
```

[More on apt package management](https://wiki.debian.org/apt)

---

## ✅ Wrapping Up

These commands are foundational for Linux-based development environments. Whether you're organizing files, managing Python projects, or working with packages, mastering these commands will make your workflow more efficient.

Practice them, and you'll become more comfortable with Linux in no time!
