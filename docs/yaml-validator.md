# YAML Validator

Validate your YAML below. This tool runs 100% in your browser—no data is sent to any server.

<div style="margin-top: 1rem;">
  <textarea id="yaml-input" style="width: 100%; height: 250px; font-family: monospace;" placeholder="Paste your YAML here..."></textarea>
</div>

<div style="margin-top: 1rem;">
  <button onclick="validateYAML()" style="padding: 0.5rem 1rem;">Validate</button>
</div>

<div style="margin-top: 1rem; background: #f7f7f7; padding: 1rem; border: 1px solid #ccc; overflow-x: auto;">
  <pre id="yaml-output">YAML validation result will appear here.</pre>
</div>

<!-- JS-YAML -->
<script src="https://cdn.jsdelivr.net/npm/js-yaml@4.1.0/dist/js-yaml.min.js"></script>
<script>
function validateYAML() {
  const input = document.getElementById('yaml-input').value;
  const output = document.getElementById('yaml-output');
  try {
    const result = jsyaml.load(input);
    output.textContent = '✅ Valid YAML:\n\n' + JSON.stringify(result, null, 2);
    output.style.color = 'green';
  } catch (e) {
    output.textContent = '❌ Invalid YAML:\n\n' + e.message;
    output.style.color = 'red';
  }
}
</script>
