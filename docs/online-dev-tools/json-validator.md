---
title: "JSON Validator"
description: "Validate and format JSON content with real-time feedback"
tags: ["tools", "json", "validator", "formatting"]
---

# JSON Validator

A real-time JSON validator and formatter. Paste your JSON content below to validate syntax and see the formatted structure.

## How to Use

1. **Paste JSON**: Enter your JSON content in the text area below
2. **Real-time Validation**: See immediate feedback on syntax errors
3. **Formatted Output**: View the properly formatted JSON structure

---

<div class="json-validator-container">
    <div class="input-section">
        <label for="json-input"><strong>JSON Input:</strong></label>
        <textarea id="json-input" rows="20" cols="80" placeholder="Paste your JSON content here...&#10;&#10;Example:&#10;{&#10;  &quot;name&quot;: &quot;John Doe&quot;,&#10;  &quot;age&quot;: 30,&#10;  &quot;skills&quot;: [&quot;Python&quot;, &quot;Ansible&quot;, &quot;Docker&quot;]&#10;}"></textarea>
    </div>
    
    <div class="output-section">
        <label for="json-output"><strong>Formatted Output:</strong></label>
        <pre id="json-output" class="output-display">Enter JSON content above to see the formatted result...</pre>
    </div>
</div>

<script>
document.getElementById("json-input").addEventListener("input", function() {
    const input = this.value.trim();
    const output = document.getElementById("json-output");
    
    if (!input) {
        output.textContent = "Enter JSON content above to see the formatted result...";
        output.className = "output-display";
        return;
    }
    
    try {
        const parsed = JSON.parse(input);
        output.textContent = JSON.stringify(parsed, null, 2);
        output.className = "output-display success";
    } catch (e) {
        output.textContent = "Error: " + e.message;
        output.className = "output-display error";
    }
});
</script>

<style>
.json-validator-container {
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

#json-input {
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
    .json-validator-container {
        grid-template-columns: 1fr;
        gap: 1rem;
    }
}
</style>

---

## Features

- **Real-time Validation**: Instant feedback as you type
- **Syntax Highlighting**: Clear error messages for invalid JSON
- **Pretty Formatting**: Automatically format valid JSON
- **Responsive Design**: Works on desktop and mobile devices

## Privacy & Security

🔒 **100% Client-side**: All processing happens in your browser. No data is sent to any server or saved anywhere.

## Common JSON Structure

```json
{
  "string": "value",
  "number": 42,
  "boolean": true,
  "null": null,
  "array": [
    "item1",
    "item2",
    "item3"
  ],
  "object": {
    "nested": "value",
    "deep": {
      "level": 3
    }
  }
}
```

## JSON Syntax Rules

- **Strings**: Must be enclosed in double quotes
- **Numbers**: Can be integers or decimals
- **Booleans**: `true` or `false` (lowercase)
- **Null**: `null` (lowercase)
- **Arrays**: Enclosed in square brackets `[]`
- **Objects**: Enclosed in curly braces `{}`
- **Commas**: Separate elements, no trailing comma
- **Quotes**: Property names must be in double quotes

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `Unexpected token` | Missing quotes around strings | Use `"value"` instead of `value` |
| `Unexpected end of JSON` | Missing closing bracket/brace | Check all brackets are closed |
| `Unexpected number` | Number at start of object | Add property name: `"key": 123` |
| `Trailing comma` | Comma after last element | Remove trailing comma | 