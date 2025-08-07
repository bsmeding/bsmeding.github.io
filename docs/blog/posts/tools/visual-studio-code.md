---
title: Visual Studio Code for Network Automation
authors: [bsmeding]
date: 2024-08-10
summary: Set up Visual Studio Code for network automation development. Learn about essential extensions, settings, and workflows for Ansible and network automation.
tags:
  - visual studio code
  - vscode
  - ide
  - development
  - automation
---

# Visual Studio Code for Network Automation

<img src="https://code.visualstudio.com/assets/docs/getstarted/userinterface/hero.png" alt="VS Code Logo" class="tool-image">

**Visual Studio Code (VS Code)** is a powerful, free code editor that's perfect for network automation development. With the right extensions and configuration, it becomes an excellent IDE for Ansible, Python, and network automation workflows.

<!-- more -->

## Why Visual Studio Code for Network Automation?

- **Free and Open Source**: No licensing costs
- **Cross-platform**: Works on Windows, macOS, and Linux
- **Extensible**: Rich ecosystem of extensions
- **Integrated Terminal**: Built-in terminal for running commands
- **Git Integration**: Built-in version control support
- **IntelliSense**: Smart code completion and error detection

## Installation

### Download and Install

1. **Download VS Code**: Visit [code.visualstudio.com](https://code.visualstudio.com/)
2. **Install**: Follow the installation wizard for your operating system
3. **Launch**: Open VS Code and start coding

### First Launch Setup

When you first launch VS Code, you'll see a welcome screen. You can:
- Choose a color theme
- Install recommended extensions
- Configure basic settings

## Essential Extensions for Network Automation

### Python Extensions

#### 1. **Pylance** by Microsoft
- Fast, feature-rich language support for Python
- Type checking and IntelliSense
- Auto-imports and code navigation

#### 2. **Python** by Microsoft
- Python language support
- IntelliSense, linting, debugging
- Jupyter notebook support

#### 3. **Python Debugger** by Microsoft
- Advanced debugging capabilities
- Breakpoint management
- Variable inspection

#### 4. **Python Environments** by Microsoft
- Manage multiple Python environments
- Virtual environment detection
- Interpreter switching

### Ansible Extensions

#### 5. **Ansible** by Red Hat
- Syntax highlighting for Ansible files
- IntelliSense for Ansible modules
- Validation and auto-completion

#### 6. **Ansible Vault** by Red Hat
- Encrypt and decrypt Ansible vault files
- Secure credential management
- Vault file syntax highlighting

### Git Extensions

#### 7. **GitLens** by GitKraken
- Enhanced Git capabilities
- Blame annotations
- Branch comparison
- File history and line history

#### 8. **GitHub Actions** by GitHub
- GitHub Actions workflow support
- YAML validation for workflows
- Action marketplace integration

#### 9. **GitHub Pull Requests** by GitHub
- Review pull requests directly in VS Code
- Comment and approve changes
- Merge conflict resolution

#### 10. **GitHub Repositories** by GitHub
- Clone repositories directly
- Browse GitHub repositories
- Manage remote repositories

#### 11. **Git Graph** by mhutchie
- Visualize Git repository history
- Interactive commit graph
- Branch visualization

### Formatters and Syntax Support

#### 12. **YAML** by Red Hat
- Syntax highlighting for YAML files
- Validation and formatting
- Essential for Ansible playbooks

#### 13. **TextFSM Template Syntax** by Cisco
- Syntax highlighting for TextFSM templates
- Network device output parsing
- Template validation

#### 14. **markdownlint** by David Anson
- Markdown linting and validation
- Consistent markdown formatting
- Style enforcement

#### 15. **Jinja** by Wholroyd
- Jinja2 template syntax highlighting
- Support for Ansible templates
- Template validation

#### 16. **Shell Format** by Foxundermoon
- Shell script formatting
- Bash, Zsh, and other shell syntax
- Code style consistency

### Remote API Testing

#### 17. **Postman** by Postman
- REST API testing and development
- Request/response management
- API documentation

### Container and Infrastructure Extensions

#### 18. **Docker** by Microsoft
- Docker container management
- Dockerfile syntax highlighting
- Container lifecycle management

#### 19. **Kubernetes** by Microsoft
- Kubernetes manifest support
- YAML validation for K8s
- Cluster management

#### 20. **OpenTofu** by OpenTofu
- Infrastructure as Code support
- Terraform/OpenTofu syntax highlighting
- State management

### Remote Development Extensions

#### 21. **Remote - SSH** by Microsoft
- Edit files on remote servers
- Connect to network devices via SSH
- Integrated terminal for remote systems

#### 22. **Remote Explorer** by Microsoft
- Manage SSH connections
- Browse remote file systems
- Connection management

#### 23. **Remote Development** by Microsoft
- Complete remote development experience
- Extension pack for remote work
- Multi-machine development

#### 24. **Remote Repositories** by GitHub
- Clone and work with remote repositories
- GitHub integration
- Repository management

### Windows Subsystem for Linux (WSL)

#### 25. **WSL** by Microsoft
- Windows Subsystem for Linux integration
- Linux development environment
- Cross-platform development

### Network-Specific Extensions

#### 26. **Cisco IOS** by Cisco
- Syntax highlighting for Cisco IOS configurations
- Auto-completion for IOS commands
- Network device configuration support

## Installing Extensions

### Method 1: Extension Marketplace
1. Click the Extensions icon in the sidebar (or press `Ctrl+Shift+X`)
2. Search for the extension name
3. Click "Install"

### Method 2: Command Palette
1. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS)
2. Type "Extensions: Install Extensions"
3. Search and install

### Method 3: Command Line
```bash
# Install essential extensions from command line
# Python extensions
code --install-extension ms-python.python
code --install-extension ms-python.pylance
code --install-extension ms-python.debugpy

# Ansible extensions
code --install-extension redhat.ansible
code --install-extension redhat.vscode-ansible-vault

# Git extensions
code --install-extension eamodio.gitlens
code --install-extension github.vscode-github-actions
code --install-extension github.vscode-pull-request-github
code --install-extension github.remotehub
code --install-extension mhutchie.git-graph

# Formatters and syntax
code --install-extension redhat.vscode-yaml
code --install-extension cisco.textfsm
code --install-extension davidanson.vscode-markdownlint
code --install-extension wholroyd.jinja
code --install-extension foxundermoon.shell-format

# API testing
code --install-extension postman.postman

# Container and infrastructure
code --install-extension ms-azuretools.vscode-docker
code --install-extension ms-kubernetes-tools.vscode-kubernetes-tools
code --install-extension opentofu.vscode-opentofu

# Remote development
code --install-extension ms-vscode-remote.remote-ssh
code --install-extension ms-vscode-remote.remote-explorer
code --install-extension ms-vscode-remote.vscode-remote-extensionpack
code --install-extension github.remotehub

# WSL (Windows only)
code --install-extension ms-vscode-remote.remote-wsl


```

## Recommended Settings

### User Settings
Open settings with `Ctrl+,` and add these configurations:

```json
{
    // Editor settings
    "editor.tabSize": 2,
    "editor.insertSpaces": true,
    "editor.detectIndentation": false,
    "editor.rulers": [80, 120],
    "editor.wordWrap": "on",
    
    // File associations
    "files.associations": {
        "*.yml": "yaml",
        "*.yaml": "yaml",
        "*.j2": "jinja",
        "*.ios": "cisco-ios"
    },
    
    // YAML settings
    "yaml.format.enable": true,
    "yaml.validate": true,
    "yaml.schemas": {
        "https://raw.githubusercontent.com/ansible/ansible-lint/main/src/ansiblelint/schemas/ansible.json": "**/playbook.yml",
        "https://raw.githubusercontent.com/ansible/ansible-lint/main/src/ansiblelint/schemas/ansible.json": "**/tasks/*.yml"
    },
    
    // Python settings
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    
    // Terminal settings
    "terminal.integrated.defaultProfile.linux": "bash",
    "terminal.integrated.defaultProfile.windows": "PowerShell",
    "terminal.integrated.defaultProfile.osx": "zsh",
    
    // Git settings
    "git.enableSmartCommit": true,
    "git.confirmSync": false,
    
    // File explorer
    "explorer.confirmDelete": false,
    "explorer.confirmDragAndDrop": false
}
```

### Workspace Settings
Create `.vscode/settings.json` in your project:

```json
{
    "ansible.ansiblePath": "./venv/bin/ansible",
    "ansible.pythonPath": "./venv/bin/python",
    "python.defaultInterpreterPath": "./venv/bin/python",
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true,
        "**/.git": true,
        "**/node_modules": true
    }
}
```

## Project Structure for Network Automation

### Recommended Folder Structure
```
network-automation/
├── .vscode/
│   ├── settings.json
│   ├── launch.json
│   └── extensions.json
├── inventory/
│   ├── hosts.yml
│   └── group_vars/
├── playbooks/
│   ├── site.yml
│   └── tasks/
├── templates/
│   └── *.j2
├── roles/
│   └── custom_role/
├── scripts/
│   └── *.py
├── requirements.txt
├── ansible.cfg
└── README.md
```

### VS Code Workspace File
Create `network-automation.code-workspace`:

```json
{
    "folders": [
        {
            "name": "Network Automation",
            "path": "."
        }
    ],
    "settings": {
        "files.associations": {
            "*.yml": "yaml",
            "*.yaml": "yaml",
            "*.j2": "jinja"
        },
        "ansible.ansiblePath": "./venv/bin/ansible",
        "python.defaultInterpreterPath": "./venv/bin/python"
    },
    "extensions": {
        "recommendations": [
            "ms-python.python",
            "ms-python.pylance",
            "ms-python.debugpy",
            "redhat.ansible",
            "redhat.vscode-ansible-vault",
            "redhat.vscode-yaml",
            "eamodio.gitlens",
            "github.vscode-github-actions",
            "github.vscode-pull-request-github",
            "github.remotehub",
            "mhutchie.git-graph",
            "cisco.textfsm",
            "davidanson.vscode-markdownlint",
            "wholroyd.jinja",
            "foxundermoon.shell-format",
            "postman.postman",
            "ms-azuretools.vscode-docker",
            "ms-kubernetes-tools.vscode-kubernetes-tools",
            "opentofu.vscode-opentofu",
            "ms-vscode-remote.remote-ssh",
            "ms-vscode-remote.remote-explorer",
            "ms-vscode-remote.vscode-remote-extensionpack",
            "ms-vscode-remote.remote-wsl",
            "cisco.cisco-ios"
        ]
    }
}
```

## Useful Keyboard Shortcuts

### General
- `Ctrl+Shift+P`: Command Palette
- `Ctrl+,`: Open Settings
- `Ctrl+Shift+X`: Extensions
- `Ctrl+B`: Toggle Sidebar
- `Ctrl+J`: Toggle Terminal

### Editing
- `Ctrl+D`: Select next occurrence
- `Alt+Shift+F`: Format document
- `Ctrl+/`: Toggle comment
- `Ctrl+Z`: Undo
- `Ctrl+Shift+Z`: Redo

### Navigation
- `Ctrl+P`: Quick Open
- `Ctrl+Shift+F`: Find in files
- `Ctrl+G`: Go to line
- `F12`: Go to definition
- `Alt+F12`: Peek definition

### Terminal
- `Ctrl+``: Toggle terminal
- `Ctrl+Shift+``: New terminal
- `Ctrl+Shift+5`: Split terminal

## Integrated Terminal Usage

### Opening Terminal
- `Ctrl+`` (backtick)
- Or View → Terminal

### Terminal Commands for Network Automation
```bash
# Activate virtual environment
source venv/bin/activate

# Run Ansible playbook
ansible-playbook -i inventory/hosts.yml playbooks/site.yml

# Check syntax
ansible-playbook --syntax-check playbooks/site.yml

# Dry run
ansible-playbook --check playbooks/site.yml

# Run with verbose output
ansible-playbook -v playbooks/site.yml
```

## Debugging and Testing

### Python Debugging
1. Set breakpoints by clicking left of line numbers
2. Press `F5` to start debugging
3. Use debug console to inspect variables

### Ansible Playbook Testing
```bash
# Syntax check
ansible-playbook --syntax-check playbook.yml

# Dry run
ansible-playbook --check playbook.yml

# Verbose output
ansible-playbook -vvv playbook.yml
```

## Git Integration

### Basic Git Operations
- **Stage Changes**: Click the + next to modified files
- **Commit**: Enter commit message and press `Ctrl+Enter`
- **Push/Pull**: Use the sync button in status bar
- **Branch**: Click branch name in status bar to switch

### GitLens Features
- **Blame**: See who changed each line
- **File History**: View file change history
- **Branch Comparison**: Compare branches visually

## Remote Development

### SSH Remote Development
1. Install "Remote - SSH" extension
2. Press `Ctrl+Shift+P` and select "Remote-SSH: Connect to Host"
3. Enter SSH connection string: `user@hostname`
4. VS Code will connect and open remote workspace

### Example SSH Config
Add to `~/.ssh/config`:
```
Host network-device
    HostName 192.168.1.1
    User admin
    IdentityFile ~/.ssh/id_rsa
    Port 22
```

## Productivity Tips

### 1. Use Snippets
Create custom snippets for common Ansible tasks:

```json
{
    "Ansible Task": {
        "prefix": "ansible-task",
        "body": [
            "- name: ${1:Task description}",
            "  ${2:module_name}:",
            "    ${3:parameter}: ${4:value}"
        ]
    }
}
```

### 2. Use Multi-Cursor Editing
- `Alt+Click`: Add cursor at click position
- `Ctrl+Alt+Up/Down`: Add cursor above/below
- `Ctrl+D`: Select next occurrence

### 3. Use Split Editor
- `Ctrl+\`: Split editor right
- `Ctrl+K Ctrl+\`: Split editor down

### 4. Use IntelliSense
- `Ctrl+Space`: Trigger suggestions
- `Ctrl+Shift+Space`: Trigger parameter hints

## Troubleshooting

### Common Issues

#### Extension Not Working
1. Reload VS Code: `Ctrl+Shift+P` → "Developer: Reload Window"
2. Check extension is enabled
3. Check for conflicts with other extensions

#### Python Interpreter Issues
1. `Ctrl+Shift+P` → "Python: Select Interpreter"
2. Choose correct virtual environment
3. Restart VS Code

#### Ansible Path Issues
1. Verify Ansible is installed in virtual environment
2. Check `ansible.ansiblePath` setting
3. Ensure virtual environment is activated

## Learn More

- [VS Code Documentation](https://code.visualstudio.com/docs)
- [VS Code User Guide](https://code.visualstudio.com/learn)
- [VS Code Keyboard Shortcuts](https://code.visualstudio.com/shortcuts/keyboard-shortcuts-windows.pdf)

---

## Next Steps

Once VS Code is set up, explore:
- [Linux Basics for Network Automation](/blog/posts/tools/linux/)
- [Ansible Introduction & Getting Started](/blog/posts/tools/ansible/)
- [Git Basics for Version Control](/blog/posts/tools/git/) 