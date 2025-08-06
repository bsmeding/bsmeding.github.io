---
title: "YAML Validator"
description: "Validate and format YAML content with real-time feedback"
tags: ["tools", "yaml", "validator", "formatting"]
---

# YAML Validator

A real-time YAML validator and formatter. Paste your YAML content below to validate syntax and see the parsed structure.

## How to Use

1. **Paste YAML**: Enter your YAML content in the text area below
2. **Real-time Validation**: See immediate feedback on syntax errors
3. **Parsed Output**: View the parsed JSON structure of your YAML

---

<div class="yaml-validator-container">
    <div class="input-section">
        <label for="yaml-input"><strong>YAML Input:</strong></label>
        <textarea id="yaml-input" rows="20" cols="80" placeholder="Paste your YAML content here...&#10;&#10;Example:&#10;name: John Doe&#10;age: 30&#10;skills:&#10;  - Python&#10;  - Ansible&#10;  - Docker"></textarea>
    </div>
    
    <div class="output-section">
        <label for="yaml-output"><strong>Parsed Output:</strong></label>
        <pre id="yaml-output" class="output-display">Enter YAML content above to see the parsed result...</pre>
    </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/js-yaml@4.1.0/dist/js-yaml.min.js"></script>
<script>
document.getElementById("yaml-input").addEventListener("input", function() {
    const input = this.value.trim();
    const output = document.getElementById("yaml-output");
    
    if (!input) {
        output.textContent = "Enter YAML content above to see the parsed result...";
        output.className = "output-display";
        return;
    }
    
    try {
        const parsed = jsyaml.load(input);
        output.textContent = JSON.stringify(parsed, null, 2);
        output.className = "output-display success";
    } catch (e) {
        output.textContent = "Error: " + e.message;
        output.className = "output-display error";
    }
});
</script>

<style>
.yaml-validator-container {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
    margin: 2rem 0;
}

.input-section, .output-section {
    display: flex;
    flex-direction: column;
}

.input-section label, .output-section label {
    margin-bottom: 0.5rem;
    font-weight: bold;
}

#yaml-input {
    width: 100%;
    min-height: 400px;
    font-family: 'Roboto Mono', monospace;
    font-size: 14px;
    padding: 1rem;
    border: 2px solid #e0e0e0;
    border-radius: 4px;
    resize: vertical;
}

.output-display {
    width: 100%;
    min-height: 400px;
    font-family: 'Roboto Mono', monospace;
    font-size: 14px;
    padding: 1rem;
    border: 2px solid #e0e0e0;
    border-radius: 4px;
    background-color: #f8f9fa;
    overflow: auto;
    white-space: pre-wrap;
}

.output-display.success {
    border-color: #28a745;
    background-color: #f8fff9;
}

.output-display.error {
    border-color: #dc3545;
    background-color: #fff8f8;
    color: #dc3545;
}

@media (max-width: 768px) {
    .yaml-validator-container {
        grid-template-columns: 1fr;
        gap: 1rem;
    }
}
</style>

---

## Features

- **Real-time Validation**: Instant feedback as you type
- **Syntax Highlighting**: Clear error messages for invalid YAML
- **JSON Output**: See the parsed structure in JSON format
- **Responsive Design**: Works on desktop and mobile devices

## Common YAML Syntax

```yaml
# Basic structure
name: value
number: 42
boolean: true

# Lists
fruits:
  - apple
  - banana
  - orange

# Nested objects
person:
  name: John Doe
  age: 30
  address:
    street: 123 Main St
    city: Anytown
    zip: 12345

# Multi-line strings
description: |
  This is a multi-line
  string that preserves
  line breaks
``` 