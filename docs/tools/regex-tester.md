---
title: "Regex Tester"
description: "Test regular expressions with real-time matching and validation"
tags: ["tools", "regex", "testing", "validation"]
---

# Regex Tester

A real-time regular expression tester. Enter your regex pattern and test text to see matches instantly.

## How to Use

1. **Enter Regex**: Type your regular expression pattern in the first field
2. **Add Test Text**: Enter the text you want to test against
3. **See Results**: View matches in real-time as you type

---

<div class="regex-tester-container">
    <div class="input-section">
        <label for="regex-input"><strong>Regular Expression:</strong></label>
        <input id="regex-input" type="text" placeholder="Enter regex pattern (e.g., \d+, [a-z]+, \w+)">
        
        <label for="text-input"><strong>Test Text:</strong></label>
        <textarea id="text-input" rows="10" placeholder="Enter text to test against the regex...&#10;&#10;Example:&#10;Hello World 123&#10;This is a test string&#10;with numbers 456 and letters abc"></textarea>
    </div>
    
    <div class="output-section">
        <label for="regex-result"><strong>Results:</strong></label>
        <pre id="regex-result" class="result-display">Enter regex and text above to see matches...</pre>
        
        <div class="match-details">
            <div id="match-count" class="match-count">Matches: 0</div>
            <div id="match-list" class="match-list"></div>
        </div>
    </div>
</div>

<script>
function updateRegex() {
    const pattern = document.getElementById("regex-input").value;
    const text = document.getElementById("text-input").value;
    const result = document.getElementById("regex-result");
    const matchCount = document.getElementById("match-count");
    const matchList = document.getElementById("match-list");
    
    if (!pattern || !text) {
        result.textContent = "Enter regex and text above to see matches...";
        result.className = "result-display";
        matchCount.textContent = "Matches: 0";
        matchList.innerHTML = "";
        return;
    }
    
    try {
        const re = new RegExp(pattern, "g");
        const matches = [...text.matchAll(re)];
        
        if (matches.length > 0) {
            result.textContent = `Found ${matches.length} match(es):`;
            result.className = "result-display success";
            matchCount.textContent = `Matches: ${matches.length}`;
            
            const matchItems = matches.map((match, index) => 
                `<div class="match-item">
                    <span class="match-number">${index + 1}.</span>
                    <span class="match-text">"${match[0]}"</span>
                    <span class="match-position">at position ${match.index}</span>
                </div>`
            ).join("");
            matchList.innerHTML = matchItems;
        } else {
            result.textContent = "No matches found.";
            result.className = "result-display warning";
            matchCount.textContent = "Matches: 0";
            matchList.innerHTML = "";
        }
    } catch (e) {
        result.textContent = "Invalid regex: " + e.message;
        result.className = "result-display error";
        matchCount.textContent = "Matches: 0";
        matchList.innerHTML = "";
    }
}

document.getElementById("regex-input").addEventListener("input", updateRegex);
document.getElementById("text-input").addEventListener("input", updateRegex);
</script>

<style>
.regex-tester-container {
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

#regex-input {
    width: 100%;
    padding: 0.75rem;
    font-family: 'Roboto Mono', monospace;
    font-size: 14px;
    border: 2px solid #e0e0e0;
    border-radius: 4px;
    margin-bottom: 1rem;
}

#text-input {
    width: 100%;
    min-height: 200px;
    font-family: 'Roboto Mono', monospace;
    font-size: 14px;
    padding: 1rem;
    border: 2px solid #e0e0e0;
    border-radius: 4px;
    resize: vertical;
}

.result-display {
    width: 100%;
    min-height: 100px;
    font-family: 'Roboto Mono', monospace;
    font-size: 14px;
    padding: 1rem;
    border: 2px solid #e0e0e0;
    border-radius: 4px;
    background-color: #f8f9fa;
    overflow: auto;
    white-space: pre-wrap;
    margin-bottom: 1rem;
}

.result-display.success {
    border-color: #28a745;
    background-color: #f8fff9;
}

.result-display.warning {
    border-color: #ffc107;
    background-color: #fffbf0;
}

.result-display.error {
    border-color: #dc3545;
    background-color: #fff8f8;
    color: #dc3545;
}

.match-details {
    border: 1px solid #e0e0e0;
    border-radius: 4px;
    padding: 1rem;
    background-color: #f8f9fa;
}

.match-count {
    font-weight: bold;
    margin-bottom: 0.5rem;
    color: #495057;
}

.match-item {
    display: flex;
    align-items: center;
    margin-bottom: 0.5rem;
    padding: 0.5rem;
    background-color: white;
    border-radius: 4px;
    border-left: 4px solid #007bff;
}

.match-number {
    font-weight: bold;
    color: #007bff;
    margin-right: 0.5rem;
    min-width: 2rem;
}

.match-text {
    font-family: 'Roboto Mono', monospace;
    background-color: #e9ecef;
    padding: 0.25rem 0.5rem;
    border-radius: 3px;
    margin-right: 0.5rem;
}

.match-position {
    color: #6c757d;
    font-size: 0.9em;
}

@media (max-width: 768px) {
    .regex-tester-container {
        grid-template-columns: 1fr;
        gap: 1rem;
    }
}
</style>

---

## Features

- **Real-time Testing**: See results as you type
- **Match Details**: View each match with position information
- **Error Handling**: Clear error messages for invalid regex
- **Responsive Design**: Works on all devices

## Privacy & Security

🔒 **100% Client-side**: All processing happens in your browser. No data is sent to any server or saved anywhere.

## Common Regex Patterns

| Pattern | Description | Example |
|---------|-------------|---------|
| `\d+` | One or more digits | `123`, `456` |
| `[a-z]+` | One or more lowercase letters | `hello`, `world` |
| `\w+` | One or more word characters | `hello123`, `world_` |
| `\s+` | One or more whitespace characters | ` `, `\t` |
| `^` | Start of line | `^Hello` |
| `$` | End of line | `world$` |
| `.*` | Any character (zero or more) | `.*` |
| `.+` | Any character (one or more) | `.+` |
| `[0-9]{3}` | Exactly 3 digits | `123`, `456` |
| `[a-zA-Z]{2,4}` | 2-4 letters | `ab`, `xyz`, `abcd` |

## Examples

### Email Validation
```
^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$
```

### Phone Number (US)
```
^\(\d{3}\) \d{3}-\d{4}$
```

### URL Pattern
```
https?://[^\s]+
```

### Date Format (YYYY-MM-DD)
```
^\d{4}-\d{2}-\d{2}$
``` 