---
authors: [bsmeding]
date: 2025-05-18
title: Create development environment for Ansible roles
summary: I develop my Ansible roles, synced to Github, locally and test locally before the get tagged for Ansible galaxy. this is how i can develop and test without galaxy upload
tags: ["ansible", "role development", "ansible galaxy", "github action"]
toc: false
layout: single
comments: true
---

# Local Ansible Role Test Environment

I develop my Ansible roles, synced to [GitHub](https://github.com/bsmeding?tab=repositories&q=ansible_role&type=&language=&sort=), locally and test them before they get tagged for [Ansible Galaxy](https://galaxy.ansible.com/bsmeding). This blog shows how to set up a development environment in your favorite IDE (Visual Studio Code, Cursor AI, or your preference) and create a local test playbook synced to your roles—**no Galaxy upload required!**

<!-- more -->

## 1. Directory Layout

I use a folder in my home directory named `Git sync`. Inside, I have a sub-folder named `ANSIBLE_ROLES` where I clone all [my Ansible roles](https://github.com/bsmeding?tab=repositories&q=ansible_role&type=&language=&sort=) for development. Before pushing them to GitHub (and triggering a [GitHub Action for Galaxy upload](blog/posts/2025-01-06-github-action-push-to-ansible-galaxy)), I test them locally.

Here’s a visual of my test environment structure:

```
role_test_environment/
├── group_vars/
│   └── all
├── host_vars/
├── inventory.yml
├── install_nautobot.yml
├── roles/
└── link_dev_roles.sh
```

## 2. Basic Setup Files

**group_vars/all:**
```yaml
ansible_user: <your_ssh_user>
ansible_password: <your_ssh_pass>
ansible_become_method: sudo
ansible_become_pass: <your_ssh_pass>
ansible_connection: ssh
```

**inventory.yml:**
```yaml
all:
  children:
    devmachines:
      hosts:
        dev1:
          ansible_host: 172.20.10.8
```

## 3. The Magic: Linking Local Roles with Namespace

To test local, unstaged changes, I create symlinks from my development roles to the `roles/` directory in my test project. This is important because my GitHub repos are named `ansible_role_xxxx`, but for Ansible Galaxy, the namespace is `bsmeding` and the role is referenced as `bsmeding.rolename`.

**Why?**
- Ansible expects roles in the format `namespace.rolename` (e.g., `bsmeding.nautobot_docker`) for Galaxy-style usage.
- This matches how you’d reference roles in `requirements.yml` or in your playbooks.

**NOTE** that the correct `meta/main.yml` is set with `role_name` when using roles!
**NOTE** that the correct `galaxy.yml` is set in the root folder when using collections!

### Bash Script to Link Roles

Save this script as `link_dev_roles.sh` in your test project directory:

```bash
#!/bin/bash

SRC_DIR="$HOME/GitHub/ANSIBLE_ROLES_AND_COLLECTIONS"        # Folder with all your repos
DEST_DIR="./roles"                          # Your test project's roles/ folder
DEFAULT_NAMESPACE="bsmeding"
mkdir -p "$DEST_DIR"

for role_path in "$SRC_DIR"/*; do
    [ -d "$role_path" ] || continue

    # Case 1: Collection (uses .galaxy.yml)
    if [[ -f "$role_path/.galaxy.yml" ]]; then
        namespace=$(grep '^namespace:' "$role_path/.galaxy.yml" | awk '{print $2}')
        name=$(grep '^name:' "$role_path/.galaxy.yml" | awk '{print $2}')

    # Case 2: Regular Role (uses meta/main.yml)
    elif [[ -f "$role_path/meta/main.yml" ]]; then
        name=$(grep 'role_name:' "$role_path/meta/main.yml" | awk '{print $2}')
        author=$(grep 'author:' "$role_path/meta/main.yml" | awk '{print $2}')
        # fallback: get folder name if author is missing
        namespace="${author:-$DEFAULT_NAMESPACE}"
    else
        echo "⚠️  No metadata found in $role_path, skipping."
        continue
    fi

    # Validate
    if [[ -z "$namespace" || -z "$name" ]]; then
        echo "⚠️  Skipping $role_path — missing name or namespace."
        continue
    fi

    link_name="$DEST_DIR/${namespace}.${name}"
    if [ ! -L "$link_name" ]; then
        echo "🔗 Linking $link_name → $role_path"
        ln -s "$role_path" "$link_name"
    else
        echo "✔️  Link exists: $link_name"
    fi
done

```

Make it executable:
```sh
chmod +x link_dev_roles.sh
```
Run it every time you add a new folder to your `ANSIBLE_ROLES` development environment:
```sh
./link_dev_roles.sh
```

## 4. Example: Minimal Test Playbook

Here’s a simple playbook to test your role:

```yaml
- hosts: all
  become: true
  roles:
    - role: bsmeding.docker  # Ensure Docker is installed, this is not my development role, but to be shure Docker is installed
    - role: bsmeding.nautobot_docker # This is my testing Ansible role from the symlink
      vars:
        nautobot__superuser_name: admin
        nautobot__superuser_password: admin
        nautobot__superuser_api_token: "myapitoken"
```

## 5. .gitignore Advice

Add `roles/` to your `.gitignore` in the test project so you don’t accidentally commit symlinks:
```
roles/
```

## 6. Troubleshooting Tips
- **Symlinks not working?** On Windows, use WSL or Git Bash, or manually copy roles if symlinks are unsupported.
- **Permissions issues?** Ensure you have the right permissions for both source and destination directories.
- **Role not found?** Double-check the symlink names and that your playbook references the correct namespace and role name.

## 7. Related Content
- [All my Ansible roles on GitHub](https://github.com/bsmeding?tab=repositories&q=ansible_role&type=&language=&sort=)
- [My Ansible Galaxy profile](https://galaxy.ansible.com/bsmeding)
- [Automating Galaxy uploads with GitHub Actions](blog/posts/2025-01-06-github-action-push-to-ansible-galaxy)

## 8. Feedback

Have your own tips or questions? Leave a comment below or connect with me on [LinkedIn](https://www.linkedin.com/in/bartsmeding/). Happy automating!

