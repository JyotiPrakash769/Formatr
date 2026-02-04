const statusDiv = document.getElementById('status');
const logDiv = document.getElementById('logs');
const themeBtn = document.getElementById('theme-toggle');

function updateLabel(input) {
    if (input.files && input.files.length > 0) {
        const name = input.files[0].name;
        // Find the sibling label's file-name span
        const wrapper = input.parentElement;
        const nameSpan = wrapper.querySelector('.file-name');
        if (nameSpan) {
            nameSpan.textContent = name;
        }
    }
}

// Theme Logic
themeBtn.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
});

// RESIZE LOGIC (MAIN)
let originalImageWidth = 0;
let originalImageHeight = 0;
let originalFileSize = 0;

// CROSS LOGIC VARS
let crossOrigWidth = 0;
let crossOrigHeight = 0;
let crossOrigSize = 0;

function formatBytes(bytes, decimals = 2) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

/* CROSS TAB LOGIC START */
function handleResizeInputCross(input) {
    updateLabel(input);
    if (input.files && input.files[0]) {
        const file = input.files[0];
        crossOrigSize = file.size;
        const img = new Image();
        img.onload = function () {
            crossOrigWidth = this.width;
            crossOrigHeight = this.height;
            updateResizeCalcCross();
        };
        img.src = URL.createObjectURL(file);
    }
}

function updateResizeCalcCross() {
    const slider = document.getElementById('cross-resize-slider');
    const valSpan = document.getElementById('cross-resize-val');
    const feedback = document.getElementById('cross-resize-feedback');
    if (!slider || !feedback) return;

    const scale = parseInt(slider.value);
    valSpan.textContent = `${scale}%`;

    if (crossOrigWidth > 0) {
        const newW = Math.round(crossOrigWidth * (scale / 100));
        const newH = Math.round(crossOrigHeight * (scale / 100));
        const estSize = crossOrigSize * Math.pow(scale / 100, 2);

        feedback.innerHTML = `
            DIMS: ${crossOrigWidth}x${crossOrigHeight} &rarr; ${newW}x${newH}<br>
            SIZE: ${formatBytes(crossOrigSize)} &rarr; ~${formatBytes(estSize)}
        `;
    } else {
        feedback.textContent = "ORIGINAL: - | NEW: -";
    }
}

function updateCrossFormAction(select) {
    // Determine the action URL based on selection
    // This is handled in submit via 'handleConvert(..., true)' custom logic check
    // Actually, simplest way: change form attribute? No, handleConvert takes url arg.
    // The onsubmit in HTML is: handleConvert(event, '/api/convert/image-to-pdf', true)
    // We update that logic to read the select value.
}
/* CROSS TAB LOGIC END */

function handleResizeInput(input) {
    updateLabel(input);

    if (input.files && input.files[0]) {
        const file = input.files[0];
        originalFileSize = file.size; // Capture size
        const img = new Image();
        img.onload = function () {
            originalImageWidth = this.width;
            originalImageHeight = this.height;
            updateResizeCalc();
        };
        img.src = URL.createObjectURL(file);
    }
}

function updateResizeCalc() {
    const slider = document.getElementById('resize-slider');
    const valSpan = document.getElementById('resize-val');
    const feedback = document.getElementById('resize-feedback');

    if (!slider || !feedback) return;

    const scale = parseInt(slider.value);
    valSpan.textContent = `${scale}%`;

    if (originalImageWidth > 0 && originalImageHeight > 0) {
        const newW = Math.round(originalImageWidth * (scale / 100));
        const newH = Math.round(originalImageHeight * (scale / 100));

        // Rough estimation: Size change proportional to area change (squared scale)
        // This is heuristic; compression adds variability.
        const estimatedSize = originalFileSize * Math.pow(scale / 100, 2);

        const oldSizeStr = formatBytes(originalFileSize);
        const newSizeStr = formatBytes(estimatedSize);

        feedback.innerHTML = `
            DIMS: ${originalImageWidth}x${originalImageHeight} &rarr; ${newW}x${newH}<br>
            SIZE: ${oldSizeStr} &rarr; ~${newSizeStr}
        `;
    } else {
        feedback.textContent = "ORIGINAL: - | NEW: -";
    }
}

// PDF QUALITY LOGIC
function updatePdfQuality(slider) {
    const valSpan = document.getElementById('pdf-quality-val');
    const hiddenInput = document.getElementById('pdf-level-input');
    const val = parseInt(slider.value);

    let label = "MEDIUM";
    let level = "medium";

    if (val < 33) {
        label = "LOW (MAX COMPRESSION)";
        level = "high"; // confusing naming in backend, but "high" compression means low quality/size
    } else if (val > 66) {
        label = "HIGH (BEST QUALITY)";
        level = "low"; // "low" compression means high quality
    } else {
        label = "MEDIUM";
        level = "medium";
    }

    valSpan.textContent = label;
    hiddenInput.value = level;
}

function log(msg) {
    const time = new Date().toLocaleTimeString();
    logDiv.textContent += `\n[${time}] ${msg}`;
    logDiv.scrollTop = logDiv.scrollHeight;
}

function showPanel(id) {
    document.querySelectorAll('.panel').forEach(p => {
        p.style.display = 'none';
        p.classList.remove('active-panel');
    });
    document.querySelectorAll('.nav-btn').forEach(b => {
        b.classList.remove('active')
    });

    const activePanel = document.getElementById(`panel-${id}`);
    activePanel.style.display = 'flex';
    // Small timeout to allow display:flex to apply before adding animation class
    setTimeout(() => activePanel.classList.add('active-panel'), 10);

    // Find button that calls this and add active class 
    // We iterate to find the matching button or rely on event
    if (event && event.target && event.target.classList.contains('nav-btn')) {
        event.target.classList.add('active');
    }
}

// DRAG AND DROP VISUALS
document.querySelectorAll('.custom-file-label').forEach(label => {
    ['dragenter', 'dragover'].forEach(eventName => {
        label.addEventListener(eventName, e => {
            e.preventDefault();
            e.stopPropagation();
            label.classList.add('drag-over');
        }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        label.addEventListener(eventName, e => {
            e.preventDefault();
            e.stopPropagation();
            label.classList.remove('drag-over');
        }, false);
    });

    label.addEventListener('drop', e => {
        const fileInput = label.parentElement.querySelector('input');
        fileInput.files = e.dataTransfer.files;
        updateLabel(fileInput);
    });
});

async function checkHealth() {
    try {
        const response = await fetch('/api/status');
        const data = await response.json();

        if (data.status === 'running') {
            statusDiv.textContent = "ONLINE";
        }
    } catch (e) {
        statusDiv.textContent = "OFFLINE";
    }
}

// TOAST LOGIC
function showToast(msg) {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = `// ${msg}`; // Brutalist prefix

    container.appendChild(toast);

    // Remove after 3 seconds
    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s forwards';
        setTimeout(() => {
            if (container.contains(toast)) container.removeChild(toast);
        }, 300);
    }, 3000);
}

async function openOutputFolder() {
    try {
        await fetch('/api/open-output-folder', { method: 'POST' });
    } catch (e) {
        log("ERROR: COULD NOT OPEN FOLDER");
    }
}

async function handleConvert(event, url, isDynamic = false) {
    event.preventDefault();
    const form = event.target;

    // Dynamic URL override for Cross Tab
    if (isDynamic) {
        const select = form.querySelector('select'); // Assumes one select for format
        if (select) {
            url = select.value;
        }
    }

    // Client-side validation for file input
    const fileInput = form.querySelector('input[type="file"]');
    if (fileInput && fileInput.files.length === 0) {
        alert("PLEASE SELECT A FILE FIRST.");
        return;
    }

    const formData = new FormData(form);

    // Find submit button to animate
    const submitBtn = form.querySelector('button[type="submit"]');
    if (submitBtn) submitBtn.classList.add('btn-loading');

    log(`INITIATING: ${url}...`);

    try {
        const response = await fetch(url, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const err = await response.json();
            if (err.detail) {
                const detailMsg = Array.isArray(err.detail)
                    ? err.detail.map(e => e.msg).join(', ')
                    : err.detail;
                throw new Error(detailMsg);
            }
            throw new Error(err.error || 'Unknown Error');
        }

        const blob = await response.blob();
        let filename = 'output_file';
        const disposition = response.headers.get('content-disposition');
        if (disposition && disposition.includes('filename=')) {
            filename = disposition.split('filename=')[1].split(';')[0].replace(/"/g, '').trim();
        }

        const a = document.createElement('a');
        a.href = window.URL.createObjectURL(blob);
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);

        log(`SUCCESS: Downloaded ${filename}`);
        showToast(`CONVERTED: ${filename}`); // Show Toast

    } catch (e) {
        log(`ERROR: ${e.message}`);

        // Trigger shake on the tool group container
        const toolGroup = form.closest('.tool-group');
        if (toolGroup) {
            toolGroup.classList.remove('error-shake');
            void toolGroup.offsetWidth; // trigger reflow
            toolGroup.classList.add('error-shake');
        }

        const msg = e.message.includes("soffice")
            ? "LIBREOFFICE NOT FOUND. PLEASE INSTALL IT."
            : e.message.includes("ffmpeg")
                ? "FFMPEG NOT FOUND. PLEASE INSTALL IT."
                : e.message;

        showToast(`ERROR: ${msg}`); // Toast for error too
    } finally {
        if (submitBtn) submitBtn.classList.remove('btn-loading');
    }
}

// Initial check
checkHealth();
setInterval(checkHealth, 5000);

// Show first panel by default (manual click simulation)
// Changed to Home
showPanel('home');

let currentDroppedFile = null;

async function handleTranslate(e) {
    e.preventDefault();
    const source = document.getElementById('trans-source').value;
    const target = document.getElementById('trans-target').value;
    const code = document.getElementById('code-input').value;
    const apiKey = document.getElementById('api-key').value;
    const outputArea = document.getElementById('code-output');

    if (!code) {
        showToast("PLEASE ENTER CODE");
        return;
    }

    outputArea.value = "TRANSLATING...";

    try {
        const response = await fetch('/api/dev/translate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                source_lang: source,
                target_lang: target,
                code: code,
                api_key: apiKey
            })
        });
        const data = await response.json();
        if (response.ok) {
            outputArea.value = data.result;
            showToast("TRANSLATION COMPLETE");
        } else {
            outputArea.value = "ERROR: " + data.error;
            showToast("FAILED");
        }
    } catch (e) {
        outputArea.value = "SYSTEM ERROR";
        showToast("ERROR: " + e.message);
    }
}

async function handleCodeFormat(e, type) {
    e.preventDefault();
    const form = e.target;
    const formData = new FormData(form);
    const action = formData.get('action');

    let url = '';
    if (type === 'js') {
        url = action === 'beautify' ? '/api/format/beautify-js' : '/api/format/minify-js';
    } else if (type === 'css') {
        url = action === 'beautify' ? '/api/format/beautify-css' : '/api/format/minify-css';
    } else if (type === 'html') {
        if (action === 'to-pdf') {
            url = '/api/convert/html-to-pdf';
        } else {
            url = action === 'beautify' ? '/api/format/beautify-html' : '/api/format/minify-html';
        }
    }

    if (!url) {
        showToast("INVALID ACTION");
        return;
    }

    showToast("PROCESSING...");

    try {
        const response = await fetch(url, {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            const blob = await response.blob();
            const downloadUrl = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = downloadUrl;

            const disp = response.headers.get('content-disposition');
            let filename = "formatted_file";
            if (disp && disp.includes("filename=")) {
                filename = disp.split("filename=")[1].split(";")[0].replace(/"/g, "");
            }
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            showToast("SUCCESS");
            form.reset();
            updateAllLabels();
        } else {
            const err = await response.json();
            showToast("ERROR: " + (err.error || "Failed"));
        }
    } catch (e) {
        showToast("ERROR: " + e.message);
    }
}

function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    document.getElementById('drop-zone').classList.add('drag-active');
}

function handleDragLeave(e) {
    e.preventDefault();
    e.stopPropagation();
    document.getElementById('drop-zone').classList.remove('drag-active');
}

async function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    document.getElementById('drop-zone').classList.remove('drag-active');

    const files = e.dataTransfer.files;
    if (files.length > 0) {
        currentDroppedFile = files[0];
        document.getElementById('drop-zone').style.display = 'none';
        document.getElementById('smart-actions').style.display = 'block';
        document.getElementById('smart-filename').textContent = currentDroppedFile.name;

        await analyzeFile(currentDroppedFile.name);
    }
}

async function handleSmartInput(input) {
    if (input.files && input.files.length > 0) {
        currentDroppedFile = input.files[0];
        document.getElementById('drop-zone').style.display = 'none';
        document.getElementById('smart-actions').style.display = 'block';
        document.getElementById('smart-filename').textContent = currentDroppedFile.name;

        await analyzeFile(currentDroppedFile.name);
    }
}

async function analyzeFile(filename) {
    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ filename: filename })
        });
        const data = await response.json();
        renderActions(data.actions);
    } catch (e) {
        log("ERROR ANALYZING FILE");
    }
}

function renderActions(actions) {
    const grid = document.getElementById('actions-grid');
    grid.innerHTML = '';

    actions.forEach(action => {
        const btn = document.createElement('div');
        btn.className = 'action-card';
        btn.textContent = action.name;
        btn.onclick = () => executeSmartAction(action); // Pass full action object
        grid.appendChild(btn);
    });

    // Add "Reset" button
    const reset = document.createElement('div');
    reset.className = 'action-card';
    reset.textContent = "RESET / NEW FILE";
    reset.style.background = "#fff";
    reset.style.color = "#000";
    reset.onclick = () => {
        currentDroppedFile = null;
        document.getElementById('drop-zone').style.display = 'flex';
        document.getElementById('smart-actions').style.display = 'none';
        grid.innerHTML = '';
    };
    grid.appendChild(reset);
}

async function executeSmartAction(action) {
    if (!currentDroppedFile) return;

    // Use FormData to send file
    const formData = new FormData();
    formData.append('file', currentDroppedFile);

    let url = '';

    // Map Action ID to API Endpoints
    switch (action.id) {
        case 'convert_image':
            const fmt = prompt("Enter Format (png, jpg, webp, pdf):", "png");
            if (!fmt) return;
            url = '/api/convert/image';
            formData.append('target_format', fmt);
            break;
        case 'image_to_pdf':
            url = '/api/convert/image-to-pdf';
            break;
        case 'image_to_docx':
            url = '/api/convert/image-to-docx';
            break;
        case 'resize_image':
            showPanel('images');
            alert("PLEASE USE THE RESIZE TOOL IN THE IMAGES TAB");
            return;
        case 'compress_image':
            url = '/api/compress/image';
            const size = prompt("Target Size (KB):", "500");
            formData.append('size_kb', size || 500);
            break;
        case 'compress_pdf':
            url = '/api/compress/pdf';
            formData.append('level', 'medium');
            break;
        case 'pdf_to_image':
            url = '/api/convert/pdf-to-image';
            formData.append('format', 'png');
            break;
        case 'doc_to_pdf':
            url = '/api/convert/doc';
            formData.append('target_format', 'pdf');
            break;
        case 'extract_audio':
            url = '/api/extract/audio';
            formData.append('format', 'mp3');
            break;
        case 'convert_video':
            const vfmt = prompt("Target format (mp4, mkv, avi):", "mp4");
            url = '/api/convert/media';
            formData.append('target_format', vfmt || 'mp4');
            break;
        case 'convert_audio':
            const afmt = prompt("Target format (mp3, wav):", "mp3");
            url = '/api/convert/media';
            formData.append('target_format', afmt || 'mp3');
            break;
        case 'convert_archive':
            const arfmt = prompt("Target format (zip, tar, gztar):", "zip");
            if (!arfmt) return;
            url = '/api/convert/archive';
            formData.append('target_format', arfmt);
            break;
        case 'md_to_pdf':
            url = '/api/dev/md-to-pdf';
            break;
        case 'convert_config':
            const cfmt = prompt("Target format (json, yaml, xml):", "json");
            if (!cfmt) return;
            url = '/api/dev/convert-config';
            formData.append('target_format', cfmt);
            break;
        case 'base64_encode':
            url = '/api/dev/base64';
            formData.append('action', 'encode');
            break;
        case 'base64_decode':
            url = '/api/dev/base64';
            formData.append('action', 'decode');
            break;
        // PHASE 1 ADDITIONS
        case 'csv_to_json':
            url = '/api/convert/csv-to-json';
            break;
        case 'json_to_csv':
            url = '/api/convert/json-to-csv';
            break;
        case 'csv_to_excel':
            url = '/api/convert/csv-to-excel';
            break;
        case 'video_to_gif':
            const gifFps = prompt("FPS (frames per second, 5-15 recommended):", "10");
            const gifWidth = prompt("Width in pixels (480-720 recommended):", "480");
            url = '/api/convert/video-to-gif';
            formData.append('fps', gifFps || 10);
            formData.append('width', gifWidth || 480);
            break;
        case 'beautify_js':
            url = '/api/format/beautify-js';
            break;
        case 'minify_js':
            url = '/api/format/minify-js';
            break;
        case 'beautify_css':
            url = '/api/format/beautify-css';
            break;
        case 'minify_css':
            url = '/api/format/minify-css';
            break;
        case 'beautify_html':
            url = '/api/format/beautify-html';
            break;
        case 'minify_html':
            url = '/api/format/minify-html';
            break;
        case 'html_to_pdf':
            url = '/api/convert/html-to-pdf';
            break;

        // Phase 2 Tier 1 Actions
        case 'excel_to_csv':
            url = '/api/convert/excel-to-csv';
            break;
        case 'excel_to_json':
            url = '/api/convert/excel-to-json';
            break;
        case 'xls_to_xlsx':
            url = '/api/convert/xls-to-xlsx';
            break;
        case 'extract_pptx_images':
            url = '/api/extract/pptx-images';
            break;
        case 'extract_pptx_text':
            url = '/api/extract/pptx-text';
            break;
        case 'pptx_info':
            url = '/api/info/pptx';
            break;
        case 'toml_to_json':
            url = '/api/convert/toml-to-json';
            break;
        case 'toml_to_yaml':
            url = '/api/convert/toml-to-yaml';
            break;
        case 'env_to_json':
            url = '/api/convert/env-to-json';
            break;
        case 'validate_env':
            url = '/api/validate/env';
            break;
        case '7z_to_zip':
            url = '/api/convert/7z-to-zip';
            break;

        default:
            if (action.id.startsWith('extract')) {
                url = '/api/extract/images';
            } else {
                alert("Automated action not linked. Please use specific tab.");
                return;
            }
    }

    if (url) {
        showToast(`EXECUTING: ${action.name}`);
        // Send request
        try {
            const response = await fetch(url, { method: 'POST', body: formData });
            if (response.ok) {
                const blob = await response.blob();
                const downloadUrl = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = downloadUrl;
                // Get filename header
                const disp = response.headers.get('content-disposition');
                let filename = "output";
                if (disp && disp.includes("filename=")) {
                    filename = disp.split("filename=")[1].split(";")[0].replace(/"/g, "");
                }
                a.download = filename;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                showToast("SUCCESS");
            } else {
                const err = await response.json();
                showToast("ERROR: " + (err.error || "Failed"));
            }
        } catch (e) {
            showToast("ERROR: " + e.message);
        }
    }
}
