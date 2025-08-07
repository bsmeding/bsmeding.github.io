---
title: Linux Basics for Network Automation
authors: [bsmeding]
date: 2024-08-10
summary: Essential Linux commands and concepts for network automation beginners. Learn the basics needed to work with automation tools.
tags:
  - linux
  - basics
  - command line
  - automation
---

# Linux Basics for Network Automation

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Tux.svg/300px-Tux.svg.png" alt="Linux Logo" width="200" style="display: block; margin: 0 auto;">

**Linux** is the foundation of most network automation tools. Understanding basic Linux commands and concepts is essential for anyone starting with network automation.

<!-- more -->

## Why Linux for Network Automation?

- Most automation tools run on Linux
- Command-line efficiency for automation workflows
- Better integration with development tools
- Cost-effective and open-source

## Essential Commands for Network Automation

### File and Directory Management

```bash
# Navigate directories
cd /path/to/directory    # Change directory
pwd                      # Print working directory
ls -la                   # List files with details

# Create and manage files
mkdir automation         # Create directory
touch playbook.yml       # Create empty file
cp source dest           # Copy files
mv old_name new_name     # Move/rename files
rm filename              # Remove file
rm -rf directory         # Remove directory recursively
```

### File Editing

```bash
# Text editors (choose one)
nano playbook.yml        # Simple editor for beginners
vim playbook.yml         # Advanced editor
code playbook.yml        # Visual Studio Code (if installed)
```

### File Permissions

```bash
# View permissions
ls -la

# Change permissions
chmod +x script.sh       # Make executable
chmod 600 private_key    # Secure private key
chown user:group file    # Change ownership
```

### Package Management

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install package_name

# CentOS/RHEL
sudo yum install package_name
# or
sudo dnf install package_name

# Python packages
pip install ansible
pip install --user ansible  # Install for current user only
```

### Process Management

```bash
# View running processes
ps aux | grep ansible
top                        # Interactive process viewer
htop                       # Enhanced top (if installed)

# Kill processes
kill process_id
killall process_name
```

### Network Commands

```bash
# Network connectivity
ping 192.168.1.1
ssh user@hostname
scp file user@hostname:/path/
wget https://example.com/file
curl https://api.example.com/data

# Network information
ip addr show
ip route show
netstat -tuln
ss -tuln
```

### Environment and Variables

```bash
# View environment variables
env
echo $PATH
echo $HOME

# Set variables
export ANSIBLE_HOST_KEY_CHECKING=False
export EDITOR=nano

# Persistent variables (add to ~/.bashrc)
echo 'export ANSIBLE_HOST_KEY_CHECKING=False' >> ~/.bashrc
source ~/.bashrc
```

## Working with Text Files

### Viewing Files

```bash
# View entire file
cat filename

# View file page by page
less filename
more filename

# View beginning/end of file
head -20 filename
tail -20 filename
tail -f logfile    # Follow log file in real-time
```

### Searching in Files

```bash
# Search for text in files
grep "search_term" filename
grep -r "search_term" directory/    # Recursive search
grep -i "search_term" filename      # Case insensitive

# Find files
find . -name "*.yml"               # Find YAML files
find . -type f -name "*.py"        # Find Python files
```

## Shell Scripting Basics

### Simple Script Example

```bash
#!/bin/bash
# This is a comment

# Variables
HOSTNAME="192.168.1.1"
USERNAME="admin"

# Commands
echo "Connecting to $HOSTNAME..."
ssh $USERNAME@$HOSTNAME "show version"
```

### Make Script Executable

```bash
chmod +x script.sh
./script.sh
```

## Virtual Environments

### Python Virtual Environment

```bash
# Create virtual environment
python3 -m venv automation_env

# Activate virtual environment
source automation_env/bin/activate    # Linux/macOS
# automation_env\Scripts\activate     # Windows

# Deactivate
deactivate

# Install packages in virtual environment
pip install ansible
pip install -r requirements.txt
```

## File System Navigation

### Common Directories

```bash
/home/username/          # User home directory
/etc/                    # System configuration
/var/log/               # Log files
/tmp/                   # Temporary files
/usr/local/bin/         # User-installed programs
```

### Path Management

```bash
# Add directory to PATH
export PATH=$PATH:/path/to/scripts

# Check if command exists
which ansible
whereis ansible
```

## Best Practices

1. **Use Tab Completion**: Press Tab to auto-complete commands and filenames
2. **Use History**: Press Up/Down arrows to navigate command history
3. **Use Aliases**: Create shortcuts for common commands
4. **Backup Important Files**: Always backup before making changes
5. **Use Absolute Paths**: When in doubt, use full paths

## Common Aliases for Network Automation

Add these to your `~/.bashrc`:

```bash
# Network automation aliases
alias ansible-playbook='ansible-playbook -i inventory'
alias ansible-inventory='ansible-inventory --list -i inventory'
alias ansible-doc='ansible-doc -t module'

# Quick navigation
alias ll='ls -la'
alias ..='cd ..'
alias ...='cd ../..'
```

## Learn More

- [Linux Command Line Tutorial](https://www.learnenough.com/command-line-tutorial)
- [Bash Scripting Guide](https://tldp.org/LDP/abs/html/)
- [Linux Journey](https://linuxjourney.com/)

---

## Next Steps

Once you're comfortable with Linux basics, explore:
- [Ansible Introduction & Getting Started](/blog/posts/tools/ansible/)
- [Visual Studio Code for Network Automation](/blog/posts/tools/visual-studio-code/)
- [Git Basics for Version Control](/blog/posts/tools/git/) 