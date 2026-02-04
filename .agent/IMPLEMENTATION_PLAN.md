# FORMATR - Universal File Format Support Implementation Plan

## Current Status (v1.0)

### ✅ Fully Implemented
- **Images**: PNG, JPG, JPEG, WEBP, BMP, TIFF, HEIC, SVG
  - Convert between formats
  - Resize/compress
  - Convert to PDF/DOCX
- **Documents**: PDF, DOCX
  - PDF compression
  - PDF ↔ Images
  - DOCX → PDF
  - Extract images from PDF/DOCX
- **Video**: MP4, MKV, MOV, AVI, WEBM
  - Video format conversion
  - Extract audio
- **Audio**: MP3, WAV, AAC, FLAC, OGG
  - Audio format conversion
- **Archives**: ZIP, TAR, GZ, TGZ
  - Archive format conversion
- **Developer**: JSON, YAML, XML, Markdown
  - Config file conversion
  - Markdown → PDF
  - Base64 encode/decode
  - AI Code Translator (experimental)

---

## Phase 1: Quick Wins (Minimal Dependencies)

### Priority: HIGH | Timeline: 1-2 days | Complexity: LOW

#### 1.1 Image Enhancements
**Format**: GIF
- **Library**: Pillow (already installed)
- **Actions**:
  - GIF ↔ PNG/JPG/WEBP
  - GIF optimization/compression
  - Extract frames from GIF
- **Implementation**: Update `ImageProcessor.convert_image()`

#### 1.2 Data File Support
**Formats**: CSV
- **Library**: `pandas` (lightweight)
- **Actions**:
  - CSV ↔ JSON
  - CSV ↔ Excel (XLSX)
  - CSV formatting/cleaning
- **New File**: `backend/core/data_processor.py`

#### 1.3 HTML Processing
**Format**: HTML
- **Library**: `xhtml2pdf` (already installed), `beautifulsoup4`
- **Actions**:
  - HTML → PDF (already possible via xhtml2pdf)
  - HTML formatting/prettify
  - HTML → Markdown
- **Enhancement**: Extend `DevProcessor`

#### 1.4 Audio Extension
**Format**: M4A
- **Library**: FFmpeg (already bundled)
- **Actions**:
  - M4A ↔ MP3/WAV/AAC
- **Implementation**: Update `AVProcessor` format list

#### 1.5 Video Extension
**Format**: FLV
- **Library**: FFmpeg (already bundled)
- **Actions**:
  - FLV ↔ MP4/MKV
  - Video → GIF (with palette optimization)
- **Implementation**: 
  - Update `AVProcessor` format list
  - Add `video_to_gif()` method

#### 1.6 Code Formatting
**Formats**: JS, CSS, HTML, JSON
- **Library**: `jsbeautifier`, `cssbeautifier`
- **Actions**:
  - Minify/Prettify JavaScript
  - Minify/Prettify CSS
  - Format HTML
  - Format JSON
- **New File**: `backend/core/code_formatter.py`

### Dependencies to Add:
```txt
pandas
beautifulsoup4
jsbeautifier
cssbeautifier
```

---

## Phase 2: Medium Priority (New Libraries Required)

### Priority: MEDIUM | Timeline: 3-5 days | Complexity: MEDIUM

#### 2.1 Microsoft Office Support
**Formats**: XLS, XLSX, PPT, PPTX
- **Libraries**: 
  - `openpyxl` (Excel read/write)
  - `python-pptx` (PowerPoint)
  - `xlrd` (legacy XLS)
- **Actions**:
  - Excel ↔ CSV/JSON
  - PowerPoint → PDF (via LibreOffice or comtypes)
  - Extract images from PowerPoint
- **Challenges**: 
  - PPT → PDF requires external tool or Windows COM
  - Consider `unoconv` or `comtypes` on Windows

#### 2.2 Advanced Archives
**Formats**: RAR, 7Z
- **Libraries**: 
  - `py7zr` (7Z)
  - `rarfile` (RAR - requires WinRAR/unrar)
- **Actions**:
  - Extract RAR/7Z
  - Convert to ZIP
- **Challenges**: 
  - RAR requires external `unrar.exe`
  - 7Z creation/extraction

#### 2.3 Developer Data Formats
**Formats**: TOML, ENV
- **Libraries**: 
  - `toml` or `tomli`
  - Custom ENV parser
- **Actions**:
  - TOML ↔ JSON/YAML
  - ENV ↔ JSON
  - ENV variable validation

#### 2.4 Advanced Code Support
**Formats**: TypeScript, JSX, SCSS
- **Libraries**: 
  - `esbuild` (via subprocess)
  - `sass` (for SCSS)
- **Actions**:
  - TypeScript → JavaScript (transpile)
  - JSX → JS
  - SCSS → CSS
- **Challenges**: 
  - Requires Node.js/npm for some tools
  - Consider bundling esbuild binary

### Dependencies to Add:
```txt
openpyxl
python-pptx
xlrd
py7zr
rarfile
tomli
sass
```

---

## Phase 3: Advanced Features (Heavy Dependencies)

### Priority: LOW | Timeline: 1-2 weeks | Complexity: HIGH

#### 3.1 LibreOffice Formats
**Formats**: ODT, ODS, ODP
- **Approach**: 
  - Option A: Bundle LibreOffice portable + `unoconv`
  - Option B: Use `odfpy` for reading only
- **Actions**:
  - ODT/ODS/ODP → PDF
  - ODT → DOCX
- **Challenges**: 
  - Large bundle size (LibreOffice ~200MB)
  - Complex setup

#### 3.2 LaTeX Support
**Format**: LaTeX (.tex)
- **Approach**: Bundle MiKTeX portable or TinyTeX
- **Actions**:
  - LaTeX → PDF
  - Markdown → LaTeX
- **Challenges**: 
  - TeX distribution is 100MB+
  - Complex compilation process

#### 3.3 Database & Big Data
**Formats**: SQL, PARQUET
- **Libraries**: 
  - `sqlparse` (SQL formatting)
  - `pyarrow` (Parquet)
  - `duckdb` (SQL execution)
- **Actions**:
  - SQL formatting/validation
  - Parquet ↔ CSV/JSON
  - SQL → CSV (query execution)
- **Challenges**: 
  - Large dependencies (pyarrow ~50MB)
  - Security concerns with SQL execution

#### 3.4 RTF Support
**Format**: RTF
- **Libraries**: 
  - `striprtf` (RTF → plain text)
  - `pypandoc` (universal converter)
- **Actions**:
  - RTF → DOCX/PDF/TXT
- **Challenges**: 
  - Limited Python RTF libraries
  - May require Pandoc binary

### Dependencies to Add:
```txt
odfpy
sqlparse
pyarrow
duckdb
striprtf
# External: LibreOffice, Pandoc, TeX
```

---

## Implementation Strategy

### Phase 1 Execution Plan (Starting Now)

#### Step 1: Update Dependencies
```bash
pip install pandas beautifulsoup4 jsbeautifier cssbeautifier
```

#### Step 2: Create New Processors
1. `backend/core/data_processor.py` - CSV/data handling
2. `backend/core/code_formatter.py` - Code prettify/minify
3. Extend `backend/core/image_processor.py` - Add GIF support
4. Extend `backend/core/av_processor.py` - Add M4A, FLV, video→GIF

#### Step 3: Update Smart Detector
Add new file types to `smart_detector.py`:
- GIF, CSV, HTML, M4A, FLV, JS, CSS

#### Step 4: Create API Endpoints
Add routes in `backend/api.py`:
- `/api/convert/csv`
- `/api/format/code`
- `/api/convert/video-to-gif`
- `/api/convert/html-to-pdf`

#### Step 5: Update Frontend
- Add new panels/forms for CSV, code formatting
- Update smart actions for new formats

#### Step 6: Update Build
- Add new dependencies to `requirements.txt`
- Test PyInstaller build with new libraries

---

## Testing Checklist

### Phase 1 Tests
- [ ] GIF → PNG/JPG conversion
- [ ] GIF optimization
- [ ] CSV → JSON conversion
- [ ] CSV → Excel conversion
- [ ] HTML → PDF conversion
- [ ] HTML prettify
- [ ] JavaScript minify/prettify
- [ ] CSS minify/prettify
- [ ] M4A → MP3 conversion
- [ ] FLV → MP4 conversion
- [ ] Video → GIF conversion

### Build Tests
- [ ] All new dependencies bundle correctly
- [ ] No missing DLL errors
- [ ] Executable size acceptable (<500MB)
- [ ] All features work in frozen app

---

## Risk Assessment

### Low Risk (Phase 1)
- ✅ All libraries are pure Python or already bundled
- ✅ Small dependency footprint
- ✅ Well-documented libraries

### Medium Risk (Phase 2)
- ⚠️ Excel/PowerPoint may have COM dependencies on Windows
- ⚠️ RAR requires external binary
- ⚠️ Increased bundle size

### High Risk (Phase 3)
- 🔴 LibreOffice/TeX = massive bundle size
- 🔴 Complex external tool integration
- 🔴 Platform-specific issues
- 🔴 Maintenance burden

---

## Recommended Approach

1. **Implement Phase 1 immediately** (this session)
2. **Test thoroughly** with frozen build
3. **Evaluate user feedback** before Phase 2
4. **Consider Phase 3 as optional/premium features**

---

## Success Metrics

- ✅ Support 50+ file formats
- ✅ Maintain <500MB bundle size
- ✅ <3 second conversion time for most operations
- ✅ Zero external dependencies for end users
- ✅ 100% offline functionality

---

*Last Updated: 2026-02-04*
*Version: 1.1 (Phase 1 Ready)*
