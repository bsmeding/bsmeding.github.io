---
authors: [bsmeding]
date: 2025-01-06
title: Automatically push Ansible role to Ansible Galaxy with GitHub Actions
summary: Learn how to automate publishing your Ansible role to Ansible Galaxy using GitHub Actions, including setup of secrets, namespace, and workflow configuration.
tags: ["ansible", "ansible galaxy", "github action", "ci/cd", "automation"]
toc: true
layout: single
comments: true
---

# Automatically Publish Ansible Roles to Ansible Galaxy with GitHub Actions

Manually uploading your Ansible roles to [Ansible Galaxy](https://galaxy.ansible.com/) is tedious and error-prone. With GitHub Actions, you can automate this process so every new release is published automatically!

<!-- more -->
---

## 1. Prerequisites

- A GitHub repository containing a valid Ansible role (follows [Ansible Galaxy role structure](https://docs.ansible.com/ansible/latest/dev_guide/collections_galaxy_meta.html#role-directory-structure))
- An [Ansible Galaxy account](https://galaxy.ansible.com/)
- Your Galaxy namespace set up and linked to your GitHub account

---

## 2. Get Your Ansible Galaxy API Key

1. Log in to [Ansible Galaxy](https://galaxy.ansible.com/).
2. Click your profile icon → **My Content**.
3. Go to **API Key** tab.
4. Click **Create API Key** (if you don’t have one).
5. Copy the API key (you’ll need it for GitHub secrets).

---

## 3. Add the API Key as a GitHub Secret

1. In your GitHub repo, go to **Settings** → **Secrets and variables** → **Actions**.
2. Click **New repository secret**.
3. Name it: `ANSIBLE_GALAXY_API_KEY`
4. Paste your API key as the value.
5. Save.

> **Tip:** Never commit your API key to the repo! Always use secrets.

---

## 4. Ensure Your Role’s Namespace and meta/main.yml Are Correct

- Your role’s `meta/main.yml` should have the correct `namespace` and `role_name` fields. Replace `<your_namespace>` and `<your_role_name>` with your actual Galaxy namespace and role name:
    ```yaml
    galaxy_info:
      role_name: <your_role_name>
      namespace: <your_namespace>
      # ... other metadata ...
    ```

- The GitHub repo name should match the Galaxy role convention:  
  `ansible_role_<role_name>` (e.g., `ansible_role_nautobot_docker`).

---

## 5. Create the GitHub Actions Workflow

Create a file at `.github/workflows/galaxy-publish.yml` in your repo. Replace `<your_namespace>` with your actual Galaxy namespace:

```yaml
name: Publish Ansible Role to Galaxy

on:
  push:
    tags:
      - 'v*'  # Only run on version tags, e.g., v1.0.0

jobs:
  galaxy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.x'

      - name: Install Ansible
        run: pip install ansible

      - name: Publish to Ansible Galaxy
        env:
          ANSIBLE_GALAXY_API_KEY: ${{ secrets.ANSIBLE_GALAXY_API_KEY }}
        run: |
          ansible-galaxy role import \
            --api-key "$ANSIBLE_GALAXY_API_KEY" \
            <your_namespace> ${{ github.event.repository.name }}
```

**Notes:**
- This workflow triggers only when you push a tag starting with `v` (e.g., `v1.2.3`).
- It uses the secret for authentication.
- **Replace `<your_namespace>` with your actual Ansible Galaxy namespace.**
- If your repository name does not match your role name, adjust the last argument accordingly (e.g., use the actual role name instead of `${{ github.event.repository.name }}`).

---

## 6. Tag and Release Your Role

1. Bump the version in your role (e.g., in `meta/main.yml` or `CHANGELOG.md`).
2. Create a git tag and push it:
    ```sh
    git tag v1.0.0
    git push origin v1.0.0
    ```
3. The workflow will run and publish your role to Galaxy!

---

## 7. Troubleshooting

- **Role not appearing on Galaxy?**  
  - Check the Actions tab for errors.
  - Ensure your `meta/main.yml` has the correct namespace and role name.
  - Make sure your GitHub repo is linked to your Galaxy namespace.

- **API Key errors?**  
  - Regenerate your API key and update the GitHub secret.

- **Workflow not triggering?**  
  - Make sure you’re pushing annotated tags (`git tag v1.0.0`).

---

## 8. Best Practices

- Use [semantic versioning](https://semver.org/) for your tags.
- Keep your `meta/main.yml` up to date.
- Test your role locally before tagging and pushing.
- Use a `CHANGELOG.md` to track changes.

---

## 9. References

- [Ansible Galaxy: Importing Roles](https://docs.ansible.com/ansible/latest/dev_guide/roles_galaxy.html)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Example: bsmeding/ansible_role_nautobot_docker](https://github.com/bsmeding/ansible_role_nautobot_docker)

---

## 10. Feedback

Have questions or want to share your workflow? Leave a comment or connect with me on [LinkedIn](https://www.linkedin.com/in/bartsmeding/).

Happy automating!

