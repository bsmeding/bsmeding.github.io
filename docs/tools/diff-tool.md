---
title: "Diff Tool"
description: "Compare text differences with side-by-side highlighting"
tags: ["tools", "diff", "comparison", "text"]
---

# Diff Tool

A text comparison tool that highlights differences between two text inputs. Perfect for comparing configurations, code snippets, or any text content.

## How to Use

1. **Enter Original Text**: Paste the original version in the left text area
2. **Enter Modified Text**: Paste the modified version in the right text area
3. **View Differences**: See highlighted changes in real-time

---

<div class="diff-tool-container">
    <div class="input-section">
        <div class="text-input-group">
            <label for="original-text"><strong>Original Text:</strong></label>
            <textarea id="original-text" rows="15" placeholder="Enter original text here...&#10;&#10;Example:&#10;server {&#10;    listen 80;&#10;    server_name example.com;&#10;    root /var/www/html;&#10;}"></textarea>
        </div>
        
        <div class="text-input-group">
            <label for="modified-text"><strong>Modified Text:</strong></label>
            <textarea id="modified-text" rows="15" placeholder="Enter modified text here...&#10;&#10;Example:&#10;server {&#10;    listen 443 ssl;&#10;    server_name example.com;&#10;    root /var/www/html;&#10;    ssl_certificate /etc/ssl/certs/example.com.crt;&#10;}"></textarea>
        </div>
    </div>
    
    <div class="diff-section">
        <label for="diff-output"><strong>Differences:</strong></label>
        <div id="diff-output" class="diff-display">Enter text in both fields above to see differences...</div>
    </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/diff@5.1.0/dist/diff.min.js"></script>
<script>
function updateDiff() {
    const original = document.getElementById("original-text").value;
    const modified = document.getElementById("modified-text").value;
    const output = document.getElementById("diff-output");
    
    if (!original && !modified) {
        output.innerHTML = "Enter text in both fields above to see differences...";
        return;
    }
    
    if (!original || !modified) {
        output.innerHTML = "Please enter text in both fields to compare.";
        return;
    }
    
    try {
        const diff = Diff.diffChars(original, modified);
        let html = '';
        
        diff.forEach(part => {
            if (part.added) {
                html += `<span class="diff-added">${part.value}</span>`;
            } else if (part.removed) {
                html += `<span class="diff-removed">${part.value}</span>`;
            } else {
                html += `<span class="diff-unchanged">${part.value}</span>`;
            }
        });
        
        output.innerHTML = html || '<span class="diff-unchanged">No differences found.</span>';
    } catch (e) {
        output.innerHTML = `<span class="diff-error">Error: ${e.message}</span>`;
    }
}

document.getElementById("original-text").addEventListener("input", updateDiff);
document.getElementById("modified-text").addEventListener("input", updateDiff);
</script>

<style>
.diff-tool-container {
    display: flex;
    flex-direction: column;
    gap: 2rem;
    margin: 2rem 0;
}

.input-section {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
}

.text-input-group {
    display: flex;
    flex-direction: column;
}

.text-input-group label {
    margin-bottom: 0.5rem;
    font-weight: bold;
}

#original-text, #modified-text {
    width: 100%;
    min-height: 300px;
    font-family: 'Roboto Mono', monospace;
    font-size: 14px;
    padding: 1rem;
    border: 2px solid #e0e0e0;
    border-radius: 4px;
    resize: vertical;
}

.diff-section {
    display: flex;
    flex-direction: column;
}

.diff-section label {
    margin-bottom: 0.5rem;
    font-weight: bold;
}

.diff-display {
    width: 100%;
    min-height: 200px;
    font-family: 'Roboto Mono', monospace;
    font-size: 14px;
    padding: 1rem;
    border: 2px solid #e0e0e0;
    border-radius: 4px;
    background-color: #f8f9fa;
    overflow: auto;
    white-space: pre-wrap;
    line-height: 1.5;
}

.diff-added {
    background-color: #d4edda;
    color: #155724;
    padding: 1px 2px;
    border-radius: 2px;
}

.diff-removed {
    background-color: #f8d7da;
    color: #721c24;
    padding: 1px 2px;
    border-radius: 2px;
    text-decoration: line-through;
}

.diff-unchanged {
    color: #495057;
}

.diff-error {
    color: #dc3545;
    font-weight: bold;
}

@media (max-width: 768px) {
    .input-section {
        grid-template-columns: 1fr;
        gap: 1rem;
    }
}
</style>

---

## Features

- **Real-time Comparison**: See differences as you type
- **Character-level Diff**: Precise highlighting of changes
- **Visual Indicators**: Green for additions, red for deletions
- **Responsive Design**: Works on all devices

## Use Cases

### Configuration Comparison
Compare different versions of configuration files to see what changed.

### Code Review
Quickly identify changes between code versions.

### Text Analysis
Find differences in any text content.

### Documentation Updates
Track changes in documentation or content.

## Tips for Better Results

1. **Use Consistent Formatting**: Ensure both texts use similar formatting
2. **Include Context**: Add some surrounding text for better context
3. **Check Line Endings**: Be aware of different line ending formats
4. **Use Monospace Font**: The tool uses monospace font for better alignment

## Example Use Cases

### Nginx Configuration
Compare different nginx server block configurations.

### Ansible Playbooks
Compare different versions of Ansible playbooks.

### JSON/YAML Files
Compare configuration files in different formats.

### Log Files
Compare log outputs to identify differences. 