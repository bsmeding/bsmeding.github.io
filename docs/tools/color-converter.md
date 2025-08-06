---
title: "Color Converter"
description: "Convert between different color formats including HEX, RGB, HSL, and more"
tags: ["tools", "color", "converter", "hex", "rgb", "hsl", "css"]
---

# Color Converter

A comprehensive color converter supporting multiple formats. Convert between HEX, RGB, HSL, CMYK, and other color formats with real-time preview.

## How to Use

1. **Enter Color**: Input a color in any supported format
2. **Auto-detect**: The tool automatically detects the input format
3. **View Results**: See all equivalent color formats and preview

---

<div class="color-converter-container">
    <div class="input-section">
        <label for="color-input"><strong>Input Color:</strong></label>
        <div class="input-group">
            <input id="color-input" type="text" placeholder="Enter color (e.g., #ff0000, rgb(255,0,0), hsl(0,100%,50%))">
            <input id="color-picker" type="color" value="#ff0000">
        </div>
        
        <div class="color-preview">
            <div id="preview-box" class="preview-box"></div>
            <div id="color-name" class="color-name">Red</div>
        </div>
    </div>
    
    <div class="output-section">
        <label><strong>Color Formats:</strong></label>
        <div class="format-grid">
            <div class="format-item">
                <label>HEX</label>
                <input id="hex-output" type="text" readonly>
                <button class="copy-btn" onclick="copyToClipboard('hex-output')">📋</button>
            </div>
            
            <div class="format-item">
                <label>RGB</label>
                <input id="rgb-output" type="text" readonly>
                <button class="copy-btn" onclick="copyToClipboard('rgb-output')">📋</button>
            </div>
            
            <div class="format-item">
                <label>HSL</label>
                <input id="hsl-output" type="text" readonly>
                <button class="copy-btn" onclick="copyToClipboard('hsl-output')">📋</button>
            </div>
            
            <div class="format-item">
                <label>CMYK</label>
                <input id="cmyk-output" type="text" readonly>
                <button class="copy-btn" onclick="copyToClipboard('cmyk-output')">📋</button>
            </div>
            
            <div class="format-item">
                <label>HSV</label>
                <input id="hsv-output" type="text" readonly>
                <button class="copy-btn" onclick="copyToClipboard('hsv-output')">📋</button>
            </div>
            
            <div class="format-item">
                <label>CSS Name</label>
                <input id="css-name-output" type="text" readonly>
                <button class="copy-btn" onclick="copyToClipboard('css-name-output')">📋</button>
            </div>
        </div>
        
        <div class="color-info">
            <div id="luminance" class="info-item"></div>
            <div id="contrast" class="info-item"></div>
            <div id="accessibility" class="info-item"></div>
        </div>
    </div>
</div>

<script>
const colorInput = document.getElementById("color-input");
const colorPicker = document.getElementById("color-picker");
const previewBox = document.getElementById("preview-box");
const colorName = document.getElementById("color-name");

// Output elements
const hexOutput = document.getElementById("hex-output");
const rgbOutput = document.getElementById("rgb-output");
const hslOutput = document.getElementById("hsl-output");
const cmykOutput = document.getElementById("cmyk-output");
const hsvOutput = document.getElementById("hsv-output");
const cssNameOutput = document.getElementById("css-name-output");

// Info elements
const luminance = document.getElementById("luminance");
const contrast = document.getElementById("contrast");
const accessibility = document.getElementById("accessibility");

// CSS color names
const cssColors = {
    'aliceblue': '#f0f8ff', 'antiquewhite': '#faebd7', 'aqua': '#00ffff', 'aquamarine': '#7fffd4',
    'azure': '#f0ffff', 'beige': '#f5f5dc', 'bisque': '#ffe4c4', 'black': '#000000',
    'blanchedalmond': '#ffebcd', 'blue': '#0000ff', 'blueviolet': '#8a2be2', 'brown': '#a52a2a',
    'burlywood': '#deb887', 'cadetblue': '#5f9ea0', 'chartreuse': '#7fff00', 'chocolate': '#d2691e',
    'coral': '#ff7f50', 'cornflowerblue': '#6495ed', 'cornsilk': '#fff8dc', 'crimson': '#dc143c',
    'cyan': '#00ffff', 'darkblue': '#00008b', 'darkcyan': '#008b8b', 'darkgoldenrod': '#b8860b',
    'darkgray': '#a9a9a9', 'darkgreen': '#006400', 'darkkhaki': '#bdb76b', 'darkmagenta': '#8b008b',
    'darkolivegreen': '#556b2f', 'darkorange': '#ff8c00', 'darkorchid': '#9932cc', 'darkred': '#8b0000',
    'darksalmon': '#e9967a', 'darkseagreen': '#8fbc8f', 'darkslateblue': '#483d8b', 'darkslategray': '#2f4f4f',
    'darkturquoise': '#00ced1', 'darkviolet': '#9400d3', 'deeppink': '#ff1493', 'deepskyblue': '#00bfff',
    'dimgray': '#696969', 'dodgerblue': '#1e90ff', 'firebrick': '#b22222', 'floralwhite': '#fffaf0',
    'forestgreen': '#228b22', 'fuchsia': '#ff00ff', 'gainsboro': '#dcdcdc', 'ghostwhite': '#f8f8ff',
    'gold': '#ffd700', 'goldenrod': '#daa520', 'gray': '#808080', 'green': '#008000',
    'greenyellow': '#adff2f', 'honeydew': '#f0fff0', 'hotpink': '#ff69b4', 'indianred': '#cd5c5c',
    'indigo': '#4b0082', 'ivory': '#fffff0', 'khaki': '#f0e68c', 'lavender': '#e6e6fa',
    'lavenderblush': '#fff0f5', 'lawngreen': '#7cfc00', 'lemonchiffon': '#fffacd', 'lightblue': '#add8e6',
    'lightcoral': '#f08080', 'lightcyan': '#e0ffff', 'lightgoldenrodyellow': '#fafad2', 'lightgreen': '#90ee90',
    'lightgrey': '#d3d3d3', 'lightpink': '#ffb6c1', 'lightsalmon': '#ffa07a', 'lightseagreen': '#20b2aa',
    'lightskyblue': '#87cefa', 'lightslategray': '#778899', 'lightsteelblue': '#b0c4de', 'lightyellow': '#ffffe0',
    'lime': '#00ff00', 'limegreen': '#32cd32', 'linen': '#faf0e6', 'magenta': '#ff00ff',
    'maroon': '#800000', 'mediumaquamarine': '#66cdaa', 'mediumblue': '#0000cd', 'mediumorchid': '#ba55d3',
    'mediumpurple': '#9370db', 'mediumseagreen': '#3cb371', 'mediumslateblue': '#7b68ee', 'mediumspringgreen': '#00fa9a',
    'mediumturquoise': '#48d1cc', 'mediumvioletred': '#c71585', 'midnightblue': '#191970', 'mintcream': '#f5fffa',
    'mistyrose': '#ffe4e1', 'moccasin': '#ffe4b5', 'navajowhite': '#ffdead', 'navy': '#000080',
    'oldlace': '#fdf5e6', 'olive': '#808000', 'olivedrab': '#6b8e23', 'orange': '#ffa500',
    'orangered': '#ff4500', 'orchid': '#da70d6', 'palegoldenrod': '#eee8aa', 'palegreen': '#98fb98',
    'paleturquoise': '#afeeee', 'palevioletred': '#db7093', 'papayawhip': '#ffefd5', 'peachpuff': '#ffdab9',
    'peru': '#cd853f', 'pink': '#ffc0cb', 'plum': '#dda0dd', 'powderblue': '#b0e0e6',
    'purple': '#800080', 'red': '#ff0000', 'rosybrown': '#bc8f8f', 'royalblue': '#4169e1',
    'saddlebrown': '#8b4513', 'salmon': '#fa8072', 'sandybrown': '#f4a460', 'seagreen': '#2e8b57',
    'seashell': '#fff5ee', 'sienna': '#a0522d', 'silver': '#c0c0c0', 'skyblue': '#87ceeb',
    'slateblue': '#6a5acd', 'slategray': '#708090', 'snow': '#fffafa', 'springgreen': '#00ff7f',
    'steelblue': '#4682b4', 'tan': '#d2b48c', 'teal': '#008080', 'thistle': '#d8bfd8',
    'tomato': '#ff6347', 'turquoise': '#40e0d0', 'violet': '#ee82ee', 'wheat': '#f5deb3',
    'white': '#ffffff', 'whitesmoke': '#f5f5f5', 'yellow': '#ffff00', 'yellowgreen': '#9acd32'
};

function parseColor(input) {
    input = input.trim().toLowerCase();
    
    // HEX format
    if (input.startsWith('#')) {
        return input;
    }
    
    // CSS color name
    if (cssColors[input]) {
        return cssColors[input];
    }
    
    // RGB format
    const rgbMatch = input.match(/rgb\((\d+),\s*(\d+),\s*(\d+)\)/);
    if (rgbMatch) {
        const r = parseInt(rgbMatch[1]);
        const g = parseInt(rgbMatch[2]);
        const b = parseInt(rgbMatch[3]);
        return rgbToHex(r, g, b);
    }
    
    // RGBA format
    const rgbaMatch = input.match(/rgba\((\d+),\s*(\d+),\s*(\d+),\s*([\d.]+)\)/);
    if (rgbaMatch) {
        const r = parseInt(rgbaMatch[1]);
        const g = parseInt(rgbaMatch[2]);
        const b = parseInt(rgbaMatch[3]);
        return rgbToHex(r, g, b);
    }
    
    // HSL format
    const hslMatch = input.match(/hsl\((\d+),\s*(\d+)%,\s*(\d+)%\)/);
    if (hslMatch) {
        const h = parseInt(hslMatch[1]);
        const s = parseInt(hslMatch[2]);
        const l = parseInt(hslMatch[3]);
        return hslToHex(h, s, l);
    }
    
    // HSLA format
    const hslaMatch = input.match(/hsla\((\d+),\s*(\d+)%,\s*(\d+)%,\s*([\d.]+)\)/);
    if (hslaMatch) {
        const h = parseInt(hslaMatch[1]);
        const s = parseInt(hslaMatch[2]);
        const l = parseInt(hslaMatch[3]);
        return hslToHex(h, s, l);
    }
    
    // Short HEX
    if (/^[0-9a-f]{3}$/.test(input)) {
        return '#' + input.split('').map(c => c + c).join('');
    }
    
    // Long HEX without #
    if (/^[0-9a-f]{6}$/.test(input)) {
        return '#' + input;
    }
    
    return null;
}

function rgbToHex(r, g, b) {
    return '#' + [r, g, b].map(x => {
        const hex = x.toString(16);
        return hex.length === 1 ? '0' + hex : hex;
    }).join('');
}

function hexToRgb(hex) {
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16)
    } : null;
}

function rgbToHsl(r, g, b) {
    r /= 255;
    g /= 255;
    b /= 255;
    
    const max = Math.max(r, g, b);
    const min = Math.min(r, g, b);
    let h, s, l = (max + min) / 2;
    
    if (max === min) {
        h = s = 0;
    } else {
        const d = max - min;
        s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
        
        switch (max) {
            case r: h = (g - b) / d + (g < b ? 6 : 0); break;
            case g: h = (b - r) / d + 2; break;
            case b: h = (r - g) / d + 4; break;
        }
        h /= 6;
    }
    
    return {
        h: Math.round(h * 360),
        s: Math.round(s * 100),
        l: Math.round(l * 100)
    };
}

function hslToHex(h, s, l) {
    s /= 100;
    l /= 100;
    
    const c = (1 - Math.abs(2 * l - 1)) * s;
    const x = c * (1 - Math.abs((h / 60) % 2 - 1));
    const m = l - c / 2;
    let r = 0, g = 0, b = 0;
    
    if (0 <= h && h < 60) {
        r = c; g = x; b = 0;
    } else if (60 <= h && h < 120) {
        r = x; g = c; b = 0;
    } else if (120 <= h && h < 180) {
        r = 0; g = c; b = x;
    } else if (180 <= h && h < 240) {
        r = 0; g = x; b = c;
    } else if (240 <= h && h < 300) {
        r = x; g = 0; b = c;
    } else if (300 <= h && h < 360) {
        r = c; g = 0; b = x;
    }
    
    const rHex = Math.round((r + m) * 255).toString(16).padStart(2, '0');
    const gHex = Math.round((g + m) * 255).toString(16).padStart(2, '0');
    const bHex = Math.round((b + m) * 255).toString(16).padStart(2, '0');
    
    return '#' + rHex + gHex + bHex;
}

function rgbToCmyk(r, g, b) {
    r = r / 255;
    g = g / 255;
    b = b / 255;
    
    const k = 1 - Math.max(r, g, b);
    const c = (1 - r - k) / (1 - k);
    const m = (1 - g - k) / (1 - k);
    const y = (1 - b - k) / (1 - k);
    
    return {
        c: Math.round(c * 100),
        m: Math.round(m * 100),
        y: Math.round(y * 100),
        k: Math.round(k * 100)
    };
}

function rgbToHsv(r, g, b) {
    r /= 255;
    g /= 255;
    b /= 255;
    
    const max = Math.max(r, g, b);
    const min = Math.min(r, g, b);
    const d = max - min;
    let h, s, v = max;
    
    s = max === 0 ? 0 : d / max;
    
    if (max === min) {
        h = 0;
    } else {
        switch (max) {
            case r: h = (g - b) / d + (g < b ? 6 : 0); break;
            case g: h = (b - r) / d + 2; break;
            case b: h = (r - g) / d + 4; break;
        }
        h /= 6;
    }
    
    return {
        h: Math.round(h * 360),
        s: Math.round(s * 100),
        v: Math.round(v * 100)
    };
}

function getColorName(hex) {
    for (const [name, color] of Object.entries(cssColors)) {
        if (color.toLowerCase() === hex.toLowerCase()) {
            return name;
        }
    }
    return null;
}

function calculateLuminance(r, g, b) {
    const a = [r, g, b].map(v => {
        v /= 255;
        return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
    });
    return a[0] * 0.2126 + a[1] * 0.7152 + a[2] * 0.0722;
}

function updateColor() {
    const input = colorInput.value;
    let hex = parseColor(input);
    
    if (!hex) {
        hex = colorPicker.value;
    }
    
    const rgb = hexToRgb(hex);
    if (!rgb) return;
    
    const hsl = rgbToHsl(rgb.r, rgb.g, rgb.b);
    const cmyk = rgbToCmyk(rgb.r, rgb.g, rgb.b);
    const hsv = rgbToHsv(rgb.r, rgb.g, rgb.b);
    const colorName = getColorName(hex);
    
    // Update outputs
    hexOutput.value = hex.toUpperCase();
    rgbOutput.value = `rgb(${rgb.r}, ${rgb.g}, ${rgb.b})`;
    hslOutput.value = `hsl(${hsl.h}, ${hsl.s}%, ${hsl.l}%)`;
    cmykOutput.value = `cmyk(${cmyk.c}%, ${cmyk.m}%, ${cmyk.y}%, ${cmyk.k}%)`;
    hsvOutput.value = `hsv(${hsv.h}, ${hsv.s}%, ${hsv.v}%)`;
    cssNameOutput.value = colorName || 'N/A';
    
    // Update preview
    previewBox.style.backgroundColor = hex;
    colorName.textContent = colorName || hex.toUpperCase();
    
    // Update color picker
    colorPicker.value = hex;
    
    // Calculate luminance and contrast
    const lum = calculateLuminance(rgb.r, rgb.g, rgb.b);
    const contrastRatio = (lum + 0.05) / (0.05 + 0.05); // Against black
    
    luminance.textContent = `Luminance: ${(lum * 100).toFixed(1)}%`;
    contrast.textContent = `Contrast Ratio: ${contrastRatio.toFixed(2)}:1`;
    
    if (contrastRatio >= 4.5) {
        accessibility.textContent = 'Accessibility: ✅ Good contrast';
        accessibility.className = 'info-item good';
    } else if (contrastRatio >= 3) {
        accessibility.textContent = 'Accessibility: ⚠️ Acceptable contrast';
        accessibility.className = 'info-item warning';
    } else {
        accessibility.textContent = 'Accessibility: ❌ Poor contrast';
        accessibility.className = 'info-item poor';
    }
}

function copyToClipboard(elementId) {
    const element = document.getElementById(elementId);
    navigator.clipboard.writeText(element.value).then(() => {
        const btn = element.nextElementSibling;
        btn.textContent = '✅';
        setTimeout(() => {
            btn.textContent = '📋';
        }, 1000);
    });
}

// Event listeners
colorInput.addEventListener('input', updateColor);
colorPicker.addEventListener('input', (e) => {
    colorInput.value = e.target.value;
    updateColor();
});

// Initial setup
updateColor();
</script>

<style>
.color-converter-container {
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

.input-group {
    display: flex;
    gap: 0.5rem;
    margin-bottom: 1rem;
}

#color-input {
    flex: 1;
    padding: 0.75rem;
    font-family: 'Roboto Mono', monospace;
    font-size: 14px;
    border: 2px solid #e0e0e0;
    border-radius: 4px;
}

#color-picker {
    width: 60px;
    height: 45px;
    border: 2px solid #e0e0e0;
    border-radius: 4px;
    cursor: pointer;
}

.color-preview {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1rem;
}

.preview-box {
    width: 60px;
    height: 60px;
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.color-name {
    font-weight: bold;
    font-size: 1.1em;
    color: #495057;
}

.format-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
    margin-bottom: 1rem;
}

.format-item {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.format-item label {
    font-weight: bold;
    font-size: 0.9em;
    color: #6c757d;
}

.format-item input {
    padding: 0.5rem;
    font-family: 'Roboto Mono', monospace;
    font-size: 12px;
    border: 1px solid #e0e0e0;
    border-radius: 4px;
    background-color: #f8f9fa;
    color: #495057;
}

.copy-btn {
    padding: 0.25rem 0.5rem;
    border: none;
    border-radius: 4px;
    background-color: #007bff;
    color: white;
    cursor: pointer;
    font-size: 12px;
    transition: background-color 0.2s;
}

.copy-btn:hover {
    background-color: #0056b3;
}

.color-info {
    padding: 1rem;
    background-color: #f8f9fa;
    border-radius: 4px;
    border: 1px solid #e0e0e0;
}

.info-item {
    margin-bottom: 0.5rem;
    font-size: 0.9em;
}

.info-item.good {
    color: #28a745;
}

.info-item.warning {
    color: #ffc107;
}

.info-item.poor {
    color: #dc3545;
}

@media (max-width: 768px) {
    .color-converter-container {
        grid-template-columns: 1fr;
        gap: 1rem;
    }
    
    .format-grid {
        grid-template-columns: 1fr;
    }
    
    .input-group {
        flex-direction: column;
    }
    
    #color-picker {
        width: 100%;
        height: 50px;
    }
}
</style>

---

## Features

- **Multiple Formats**: HEX, RGB, HSL, CMYK, HSV, CSS names
- **Real-time Conversion**: Instant conversion as you type
- **Color Picker**: Visual color selection
- **Accessibility Info**: Contrast ratio and luminance
- **Copy to Clipboard**: One-click copying of any format

## Supported Formats

### HEX
- **Format**: `#RRGGBB` or `#RGB`
- **Example**: `#ff0000`, `#f00`

### RGB
- **Format**: `rgb(r, g, b)`
- **Example**: `rgb(255, 0, 0)`

### RGBA
- **Format**: `rgba(r, g, b, a)`
- **Example**: `rgba(255, 0, 0, 0.5)`

### HSL
- **Format**: `hsl(h, s%, l%)`
- **Example**: `hsl(0, 100%, 50%)`

### HSLA
- **Format**: `hsla(h, s%, l%, a)`
- **Example**: `hsla(0, 100%, 50%, 0.5)`

### CSS Color Names
- **Examples**: `red`, `blue`, `green`, `purple`

## Common Use Cases

### Web Development
Convert colors between different CSS formats.

### Design Work
Match colors across different applications.

### Accessibility
Check color contrast ratios for web accessibility.

### Print Design
Convert to CMYK for print materials.

## Color Theory

### RGB (Red, Green, Blue)
- **Use**: Digital displays, web
- **Range**: 0-255 for each component
- **Additive**: Colors are added together

### HSL (Hue, Saturation, Lightness)
- **Use**: Design, color manipulation
- **Hue**: 0-360 degrees (color wheel)
- **Saturation**: 0-100% (intensity)
- **Lightness**: 0-100% (brightness)

### CMYK (Cyan, Magenta, Yellow, Key)
- **Use**: Print materials
- **Subtractive**: Colors are subtracted from white

### HSV (Hue, Saturation, Value)
- **Use**: Color pickers, graphics software
- **Similar to HSL** but with Value instead of Lightness

## Accessibility Guidelines

### WCAG 2.1 Contrast Requirements
- **Normal text**: 4.5:1 minimum
- **Large text**: 3:1 minimum
- **UI components**: 3:1 minimum

### Luminance
- **High luminance**: Light colors
- **Low luminance**: Dark colors
- **Optimal range**: 0.05-0.95 for good contrast 