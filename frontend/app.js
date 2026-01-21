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
const firstBtn = document.querySelector('.nav-btn');
if (firstBtn) {
    showPanel('images'); // Default logic
    firstBtn.classList.add('active');
}
