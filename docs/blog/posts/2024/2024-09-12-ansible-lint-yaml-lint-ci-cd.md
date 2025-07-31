---
title: "Automate Code Quality: ansible-lint, yaml-lint, and CI/CD Integration"
date: 2024-09-12
author: bsmeding
tags: ["ansible", "ansible-lint", "yaml-lint", "ci-cd", "github-actions", "gitlab-ci", "code-quality", "automation"]
toc: true
layout: single
comments: true
---

<!-- more -->

Code quality is crucial in network automation and DevOps practices. When working with Ansible playbooks and YAML files, automated linting helps catch errors early, enforce best practices, and maintain consistent code standards. In this comprehensive guide, we'll explore how to use `ansible-lint` and `yaml-lint`, and integrate them into your CI/CD pipelines for automated code quality checks.

## What is Linting?

Linting is a static code analysis tool that checks your code for potential errors, style violations, and suspicious constructs. For Ansible and YAML files, linting helps:

- **Catch syntax errors** before deployment
- **Enforce coding standards** and best practices
- **Improve code readability** and maintainability
- **Prevent common mistakes** that could cause runtime issues
- **Ensure consistency** across team members

## ansible-lint: Ansible Code Quality Tool

[ansible-lint](https://github.com/ansible/ansible-lint) is the official linting tool for Ansible playbooks, roles, and collections. It checks your Ansible code against a set of rules and best practices.

### Installation

```bash
# Install via pip
pip install ansible-lint

# Install via package manager (Ubuntu/Debian)
sudo apt install ansible-lint

# Install via package manager (macOS)
brew install ansible-lint
```

### Basic Usage

```bash
# Lint a single playbook
ansible-lint playbook.yml

# Lint an entire directory
ansible-lint .

# Lint with specific rules
ansible-lint --rules=no-tabs,no-jinja-when playbook.yml

# Generate a report
ansible-lint --format=json playbook.yml > lint-report.json
```

### Configuration File (.ansible-lint)

Create a `.ansible-lint` file in your project root to customize linting behavior:

```yaml
---
# Enable/disable specific rules
enable_list:
  - no-tabs
  - no-jinja-when
  - no-handler
  - no-changed-when
  - no-jinja-nesting

# Disable specific rules
disable_list:
  - no-log-password  # If you need to log passwords for debugging

# Customize rule severity
warn_list:
  - no-tabs
  - no-jinja-when

# Set minimum Ansible version
min_ansible_version: "2.10"

# Customize output format
format: rich  # Options: rich, json, codeclimate, quiet, parseable

# Exclude files/directories
exclude_paths:
  - "tests/"
  - "molecule/"
  - "*.j2"

# Set custom rules directory
rulesdir: "custom_rules/"
```

### Common ansible-lint Rules

Here are some essential rules to enable:

```yaml
enable_list:
  # Code style
  - no-tabs                    # No tabs in YAML files
  - no-jinja-when             # Avoid Jinja2 in when conditions
  - no-handler                # Avoid handlers when possible
  - no-changed-when           # Always specify changed_when
  - no-jinja-nesting          # Avoid nested Jinja2 expressions
  
  # Security
  - no-log-password           # Don't log passwords
  - no-command                # Avoid raw commands
  - no-shell                  # Avoid shell module
  
  # Best practices
  - no-relative-paths         # Use absolute paths
  - no-risky-file-permissions # Avoid risky file permissions
  - no-risky-shell-pipe       # Avoid shell pipes
  - no-unsafe-reads           # Avoid unsafe file reads
```

## yaml-lint: YAML Syntax Validation

[yaml-lint](https://github.com/adrienverge/yamllint) is a Python-based linter for YAML files that checks syntax, formatting, and style.

### Installation

```bash
# Install via pip
pip install yamllint

# Install via package manager (Ubuntu/Debian)
sudo apt install yamllint

# Install via package manager (macOS)
brew install yamllint
```

### Basic Usage

```bash
# Lint a single file
yamllint playbook.yml

# Lint entire directory
yamllint .

# Lint with specific configuration
yamllint -c .yamllint playbook.yml

# Generate detailed output
yamllint --format=parsable playbook.yml
```

### Configuration File (.yamllint)

Create a `.yamllint` file to customize YAML linting rules:

```yaml
---
extends: default

rules:
  # Line length
  line-length:
    max: 120
    level: warning
    
  # Indentation
  indentation:
    spaces: 2
    indent-sequences: true
    
  # Trailing spaces
  trailing-spaces: enable
  
  # Empty lines
  empty-lines:
    max: 1
    max-end: 1
    
  # Comments
  comments:
    min-spaces-from-content: 1
    
  # Document start
  document-start: disable
  
  # Truthy values
  truthy:
    check-keys: false
    
  # Hyphens
  hyphens:
    max-spaces-before: 1
    max-spaces-after: 1
    
  # Commas
  commas:
    max-spaces-before: 0
    min-spaces-after: 1
    
  # Colons
  colons:
    max-spaces-before: 0
    max-spaces-after: 1
    
  # Braces
  braces:
    min-spaces-inside: 0
    max-spaces-inside: 1
    
  # Brackets
  brackets:
    min-spaces-inside: 0
    max-spaces-inside: 1
```

## GitHub Actions Integration

GitHub Actions provides excellent support for automated linting. Here's a comprehensive workflow:

### Complete GitHub Actions Workflow

```yaml
name: Code Quality Checks

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  lint:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.9, 3.10, 3.11]
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}
        
    - name: Cache pip dependencies
      uses: actions/cache@v4
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
        restore-keys: |
          ${{ runner.os }}-pip-
          
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install ansible ansible-lint yamllint
        
    - name: Run yamllint
      run: |
        yamllint -c .yamllint .
        
    - name: Run ansible-lint
      run: |
        ansible-lint --format=rich .
        
    - name: Upload lint results
      uses: actions/upload-artifact@v4
      if: always()
      with:
        name: lint-results-${{ matrix.python-version }}
        path: |
          lint-report.json
          yamllint-report.txt
        retention-days: 7
```

### Advanced GitHub Actions with Multiple Tools

```yaml
name: Advanced Code Quality

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  yaml-lint:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    - run: pip install yamllint
    - run: yamllint -c .yamllint .

  ansible-lint:
    runs-on: ubuntu-latest
    needs: yaml-lint
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    - run: pip install ansible ansible-lint
    - run: ansible-lint --format=rich .

  security-scan:
    runs-on: ubuntu-latest
    needs: [yaml-lint, ansible-lint]
    steps:
    - uses: actions/checkout@v4
    - name: Run Bandit security scan
      uses: python-security/bandit@main
      with:
        args: -r . -f json -o bandit-report.json
    - name: Upload security report
      uses: actions/upload-artifact@v4
      with:
        name: security-report
        path: bandit-report.json
```

## GitLab CI/CD Integration

GitLab CI/CD provides robust pipeline capabilities for linting:

### Basic GitLab CI Pipeline

```yaml
stages:
  - lint
  - test
  - deploy

variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.pip-cache"

cache:
  paths:
    - .pip-cache/

yamllint:
  stage: lint
  image: python:3.11-slim
  before_script:
    - pip install yamllint
  script:
    - yamllint -c .yamllint .
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

ansible-lint:
  stage: lint
  image: python:3.11-slim
  before_script:
    - pip install ansible ansible-lint
  script:
    - ansible-lint --format=rich .
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
  artifacts:
    reports:
      junit: ansible-lint-report.xml
    expire_in: 1 week
```

### Advanced GitLab CI with Parallel Jobs

```yaml
stages:
  - lint
  - test
  - security
  - deploy

variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.pip-cache"

cache:
  paths:
    - .pip-cache/

.yamllint_template: &yamllint_template
  stage: lint
  image: python:3.11-slim
  before_script:
    - pip install yamllint
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

yamllint-playbooks:
  <<: *yamllint_template
  script:
    - yamllint -c .yamllint playbooks/
  artifacts:
    reports:
      junit: yamllint-playbooks.xml

yamllint-roles:
  <<: *yamllint_template
  script:
    - yamllint -c .yamllint roles/
  artifacts:
    reports:
      junit: yamllint-roles.xml

.ansible_lint_template: &ansible_lint_template
  stage: lint
  image: python:3.11-slim
  before_script:
    - pip install ansible ansible-lint
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

ansible-lint-playbooks:
  <<: *ansible_lint_template
  script:
    - ansible-lint playbooks/
  artifacts:
    reports:
      junit: ansible-lint-playbooks.xml

ansible-lint-roles:
  <<: *ansible_lint_template
  script:
    - ansible-lint roles/
  artifacts:
    reports:
      junit: ansible-lint-roles.xml

security-scan:
  stage: security
  image: python:3.11-slim
  before_script:
    - pip install bandit safety
  script:
    - bandit -r . -f json -o bandit-report.json
    - safety check --json --output safety-report.json
  artifacts:
    reports:
      junit: security-report.xml
    paths:
      - bandit-report.json
      - safety-report.json
    expire_in: 1 week
```

## Pre-commit Hooks

Install pre-commit hooks to catch issues before committing:

### .pre-commit-config.yaml

```yaml
repos:
  - repo: https://github.com/ansible/ansible-lint
    rev: v6.22.1
    hooks:
      - id: ansible-lint
        args: [--format=rich]
        
  - repo: https://github.com/adrienverge/yamllint
    rev: v1.35.1
    hooks:
      - id: yamllint
        args: [-c, .yamllint]
        
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict
      - id: check-case-conflict
      - id: check-docstring-first
      - id: check-json
      - id: check-merge-conflict
      - id: debug-statements
      - id: name-tests-test
      - id: requirements-txt-fixer
      - id: fix-byte-order-marker
```

### Installation and Usage

```bash
# Install pre-commit
pip install pre-commit

# Install the git hook scripts
pre-commit install

# Run against all files
pre-commit run --all-files

# Run specific hook
pre-commit run ansible-lint --all-files
```

## Best Practices and Tips

### 1. Progressive Rule Adoption

Start with essential rules and gradually add more:

```yaml
# Start with these basic rules
enable_list:
  - no-tabs
  - no-jinja-when
  - no-log-password

# Gradually add more rules
enable_list:
  - no-tabs
  - no-jinja-when
  - no-log-password
  - no-command
  - no-shell
  - no-relative-paths
```

### 2. Custom Rules for Your Organization

Create custom rules in a `custom_rules/` directory:

```python
# custom_rules/custom_rule.py
from ansiblelint.rules import AnsibleLintRule

class CustomRule(AnsibleLintRule):
    id = 'custom-rule'
    shortdesc = 'Custom rule description'
    description = 'Detailed description of the custom rule'
    tags = ['custom']
    
    def match(self, file, line):
        # Your custom logic here
        return False
```

### 3. Integration with IDE

Configure your IDE for real-time linting:

**VS Code Settings (.vscode/settings.json):**
```json
{
    "ansible.ansibleLint.enabled": true,
    "ansible.ansibleLint.path": "ansible-lint",
    "ansible.ansibleLint.configFile": ".ansible-lint",
    "yaml.validate": true,
    "yaml.schemas": {
        "https://json.schemastore.org/ansible-stable-2.9.json": "**/tasks/*.yml",
        "https://json.schemastore.org/ansible-stable-2.9.json": "**/handlers/*.yml"
    }
}
```

### 4. Performance Optimization

For large projects, optimize linting performance:

```bash
# Use parallel processing
ansible-lint --parallel .

# Exclude unnecessary directories
ansible-lint --exclude=test/ --exclude=docs/ .

# Use specific file patterns
ansible-lint "**/*.yml" "**/*.yaml"
```

### 5. Reporting and Metrics

Generate detailed reports for analysis:

```bash
# Generate JSON report
ansible-lint --format=json . > lint-report.json

# Generate CodeClimate format
ansible-lint --format=codeclimate . > codeclimate.json

# Generate JUnit XML for CI
ansible-lint --format=junit . > ansible-lint.xml
```

## Troubleshooting Common Issues

### 1. False Positives

Handle false positives by disabling specific rules:

```yaml
# In .ansible-lint
disable_list:
  - no-log-password  # If logging is required for debugging
  - no-command       # If raw commands are necessary
```

### 2. Performance Issues

Optimize for large codebases:

```bash
# Use caching
ansible-lint --cache .ansible-lint-cache .

# Limit file types
ansible-lint --exclude="*.j2" --exclude="*.md" .

# Use specific directories
ansible-lint playbooks/ roles/
```

### 3. Integration Issues

Common CI/CD integration problems:

```yaml
# GitHub Actions - Handle failures gracefully
- name: Run ansible-lint
  run: |
    ansible-lint --format=rich . || {
      echo "Linting found issues. Check the output above."
      exit 1
    }
  continue-on-error: false
```

## Conclusion

Automated linting with `ansible-lint` and `yaml-lint` is essential for maintaining code quality in Ansible projects. By integrating these tools into your CI/CD pipelines, you can:

- **Catch errors early** in the development process
- **Enforce consistent coding standards** across your team
- **Improve code maintainability** and readability
- **Reduce deployment failures** caused by syntax errors
- **Build confidence** in your automation code

Start with basic linting rules and gradually expand your quality checks. Remember that the goal is to improve code quality, not to create unnecessary friction in your development workflow.

## Resources

- [ansible-lint Documentation](https://ansible-lint.readthedocs.io/)
- [yamllint Documentation](https://yamllint.readthedocs.io/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitLab CI/CD Documentation](https://docs.gitlab.com/ee/ci/)
- [Pre-commit Framework](https://pre-commit.com/)

For more automation and DevOps content, check out our [Ansible tutorials](/tutorials/ansible_tutorial_1_concepts/) and [network automation guides](/blog/posts/2025/2025-03-17-getting-started-network-automation.md). 