---
title: Jenkins Introduction & Getting Started
authors: [bsmeding]
date: 2024-09-01
summary: A practical introduction to Jenkins CI/CD, its main features, and how to set up your first pipeline.
tags:
  - jenkins
  - ci/cd
  - automation
  - devops
---

# Jenkins: Introduction & Getting Started

![Jenkins Logo](https://www.jenkins.io/images/logos/jenkins/jenkins.png?w=300&h=auto){: style="max-width: 300px; display: block; margin: 0 auto;"}

**Jenkins** is an open-source automation server widely used for building, testing, and deploying software through continuous integration and continuous delivery (CI/CD) pipelines.
<!-- more -->

## Why Use Jenkins?
- Automate software builds, tests, and deployments
- Integrate with hundreds of plugins for SCM, notifications, and more
- Visualize and manage complex pipelines

## How Jenkins Works
- Runs as a web application (Java-based)
- Pipelines are defined using a GUI or Jenkinsfile (Groovy syntax)
- Integrates with Git, Docker, cloud providers, and more

## Quick Start Example
1. **Install Jenkins (on Ubuntu):**
   ```bash
   sudo apt update
   sudo apt install openjdk-11-jre
   wget -q -O - https://pkg.jenkins.io/debian/jenkins.io.key | sudo apt-key add -
   sudo sh -c 'echo deb https://pkg.jenkins.io/debian binary/ > /etc/apt/sources.list.d/jenkins.list'
   sudo apt update
   sudo apt install jenkins
   sudo systemctl start jenkins
   ```
2. **Access Jenkins:**
   - Open `http://localhost:8080` in your browser
   - Follow the setup wizard
3. **Create a simple pipeline:**
   - Use the GUI or create a `Jenkinsfile`:
   ```groovy
   pipeline {
     agent any
     stages {
       stage('Hello') {
         steps {
           echo 'Hello, Jenkins!'
         }
       }
     }
   }
   ```

## Learn More
- [Jenkins Documentation](https://www.jenkins.io/doc/)
- [Getting Started Guide](https://www.jenkins.io/doc/pipeline/tour/getting-started/) 