---
title: GitLab CI/CD Introduction & Getting Started
authors: [bsmeding]
date: 2024-09-08
summary: A concise guide to GitLab CI/CD, its pipeline features, and how to automate builds and tests.
tags:
  - gitlab
  - ci/cd
  - automation
  - devops
---

# GitLab CI/CD: Introduction & Getting Started

![GitLab CI/CD Logo](https://about.gitlab.com/images/press/logo/png/gitlab-icon-rgb.png){: style="max-width: 300px; display: block; margin: 0 auto;"}

**GitLab CI/CD** is a built-in continuous integration and delivery system in GitLab, enabling you to automate builds, tests, and deployments directly from your Git repository.
<!-- more -->

## Why Use GitLab CI/CD?
- Automate testing and deployment with every commit
- Define pipelines as code in `.gitlab-ci.yml`
- Integrate with Docker, Kubernetes, and cloud providers

## How GitLab CI/CD Works
- Pipelines are triggered by changes in your repository
- Jobs and stages are defined in `.gitlab-ci.yml`
- Runners execute jobs on your infrastructure or in the cloud

## Quick Start Example
1. **Create a `.gitlab-ci.yml` in your repo:**
   ```yaml
   stages:
     - build
     - test

   build-job:
     stage: build
     script:
       - echo "Building..."

   test-job:
     stage: test
     script:
       - echo "Running tests..."
   ```
2. **Push to GitLab:**
   - The pipeline runs automatically on push
3. **View pipeline status:**
   - Go to your project’s **CI/CD > Pipelines** page

## Learn More
- [GitLab CI/CD Documentation](https://docs.gitlab.com/ee/ci/)
- [Getting Started Guide](https://docs.gitlab.com/ee/ci/quick_start/)
- [Code Quality with ansible-lint and yaml-lint](/blog/posts/2024/2024-09-12-ansible-lint-yaml-lint-ci-cd.md) - Implementing automated linting in GitLab CI/CD 