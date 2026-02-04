# Phase 2 Implementation Plan - File Format Analysis

## Overview
**Priority**: MEDIUM | **Timeline**: 3-5 days | **Complexity**: MEDIUM

Phase 2 focuses on adding support for Microsoft Office formats, advanced archives, and developer-specific data formats.

---

## 📊 Phase 2 File Formats

### 2.1 Microsoft Office Support

#### **Excel Files**
- **Formats**: `.xls`, `.xlsx`
- **Libraries Needed**:
  - `openpyxl` - Modern Excel (XLSX) read/write ✅ **Already installed!**
  - `xlrd` - Legacy Excel (XLS) reading
- **Actions**:
  - Excel → CSV
  - Excel → JSON
  - CSV → Excel (✅ already done in Phase 1)
  - Extract data from multiple sheets
  - Preserve formulas/formatting (optional)

#### **PowerPoint Files**
- **Formats**: `.ppt`, `.pptx`
- **Libraries Needed**:
  - `python-pptx` - PowerPoint manipulation
  - `comtypes` (Windows only) - For PPT → PDF conversion
- **Actions**:
  - Extract images from PowerPoint
  - Extract text from slides
  - PPTX → PDF (requires LibreOffice or Windows COM)
  - Count slides, get metadata
- **Challenges**:
  - PPT → PDF conversion is complex
  - May need external tool (LibreOffice portable)

### 2.2 Advanced Archive Formats

#### **7-Zip Archives**
- **Format**: `.7z`
- **Library**: `py7zr`
- **Actions**:
  - Extract 7Z archives
  - Create 7Z archives
  - Convert 7Z → ZIP
  - List contents
- **Status**: Pure Python, should bundle well

#### **RAR Archives**
- **Format**: `.rar`
- **Library**: `rarfile`
- **External Dependency**: Requires `unrar.exe` or WinRAR
- **Actions**:
  - Extract RAR archives (read-only)
  - List contents
  - Convert RAR → ZIP (extract + recompress)
- **Challenges**:
  - Need to bundle `unrar.exe` (~200KB)
  - RAR creation not supported (proprietary)
  - License considerations

### 2.3 Developer Data Formats

#### **TOML Configuration**
- **Format**: `.toml`
- **Library**: `tomli` (Python 3.11+) or `toml`
- **Actions**:
  - TOML → JSON
  - TOML → YAML
  - JSON/YAML → TOML
  - Validate TOML syntax
- **Status**: Lightweight, pure Python

#### **Environment Files**
- **Format**: `.env`
- **Library**: Custom parser (no external dependency needed)
- **Actions**:
  - ENV → JSON
  - JSON → ENV
  - Validate environment variables
  - Detect duplicates
  - Comment preservation
- **Status**: Easy to implement

### 2.4 Advanced Code Support

#### **TypeScript**
- **Format**: `.ts`
- **Approach**: Use `esbuild` binary (via subprocess)
- **Actions**:
  - TypeScript → JavaScript (transpile)
  - Type checking (optional)
  - Minify output
- **Challenges**:
  - Requires bundling `esbuild` binary (~10MB)
  - Node.js-based tool

#### **JSX/TSX**
- **Formats**: `.jsx`, `.tsx`
- **Approach**: Use `esbuild` binary
- **Actions**:
  - JSX → JS
  - TSX → JS
  - React component transpilation
- **Challenges**: Same as TypeScript

#### **SCSS/SASS**
- **Format**: `.scss`, `.sass`
- **Library**: `libsass` or `sass` (Dart Sass)
- **Actions**:
  - SCSS → CSS
  - SASS → CSS
  - Minify output
  - Source maps (optional)
- **Challenges**:
  - `libsass` is deprecated
  - Dart Sass requires bundling binary

---

## 📦 Dependencies Summary

### Required Libraries
```txt
# Excel Support
openpyxl          # ✅ Already installed
xlrd              # NEW - Legacy Excel

# PowerPoint Support
python-pptx       # NEW - PowerPoint files

# Archive Support
py7zr             # NEW - 7-Zip archives
rarfile           # NEW - RAR extraction

# Config Files
tomli             # NEW - TOML support (or 'toml')

# Code Processing
libsass           # NEW - SCSS compilation (optional)
```

### External Binaries (Optional)
```
unrar.exe         # For RAR extraction (~200KB)
esbuild.exe       # For TypeScript/JSX (~10MB)
```

---

## 🎯 Recommended Phase 2 Approach

### **Tier 1: Easy Wins** (Start Here)
1. ✅ **Excel (XLSX)** - openpyxl already installed
2. **TOML** - Lightweight, pure Python
3. **ENV** - Custom parser, no dependencies
4. **7-Zip** - Pure Python library

**Estimated Time**: 1-2 days  
**Bundle Size Impact**: +5MB

### **Tier 2: Medium Effort**
1. **Legacy Excel (XLS)** - Requires xlrd
2. **PowerPoint (PPTX)** - Extract only (no PDF conversion)

**Estimated Time**: 1-2 days  
**Bundle Size Impact**: +10MB

### **Tier 3: Complex** (Consider Carefully)
1. **RAR** - Requires external binary
2. **TypeScript/JSX** - Requires esbuild binary
3. **SCSS** - Requires Sass binary
4. **PPT → PDF** - Requires LibreOffice or COM

**Estimated Time**: 2-3 days  
**Bundle Size Impact**: +50-200MB  
**Complexity**: High

---

## 🚀 Quick Start: Phase 2 Tier 1

### Step 1: Install Dependencies
```bash
pip install xlrd python-pptx py7zr tomli
```

### Step 2: Create Processors
1. Extend `data_processor.py` - Add Excel XLS support
2. Create `office_processor.py` - PowerPoint handling
3. Extend `archive_processor.py` - Add 7Z support
4. Create `config_processor.py` - TOML/ENV handling

### Step 3: Update Smart Detector
Add detection for: `.xlsx`, `.xls`, `.pptx`, `.7z`, `.toml`, `.env`

### Step 4: Add API Endpoints
- `/api/convert/excel-to-json`
- `/api/extract/pptx-images`
- `/api/convert/7z-to-zip`
- `/api/convert/toml-to-json`
- `/api/convert/env-to-json`

---

## ⚠️ Challenges & Considerations

### Bundle Size
- **Current**: ~1.1GB (with Phase 1)
- **After Tier 1**: ~1.15GB (+50MB)
- **After Tier 2**: ~1.2GB (+100MB)
- **After Tier 3**: ~1.4GB (+300MB)

### External Dependencies
- **RAR**: Need to bundle `unrar.exe` and handle licensing
- **TypeScript**: Need to bundle `esbuild` binary
- **SCSS**: Need to bundle Sass binary
- **PPT → PDF**: Need LibreOffice portable (~200MB) or Windows COM

### Recommendations
1. **Start with Tier 1** - Low risk, high value
2. **Skip Tier 3** unless specifically requested
3. **Consider making Tier 3 features "premium" or "plugin-based"**
4. **Focus on extraction/reading rather than creation**

---

## 📋 Testing Checklist (Phase 2 Tier 1)

- [ ] XLSX → CSV conversion
- [ ] XLSX → JSON conversion
- [ ] XLS → CSV conversion (legacy Excel)
- [ ] PPTX image extraction
- [ ] PPTX text extraction
- [ ] 7Z extraction
- [ ] 7Z → ZIP conversion
- [ ] TOML → JSON conversion
- [ ] ENV → JSON conversion
- [ ] All features work in frozen build
- [ ] Bundle size acceptable

---

## 💡 Recommendation

**Start with Phase 2 Tier 1** for maximum value with minimal complexity:
- Excel support (already have openpyxl!)
- TOML config files
- ENV files
- 7-Zip archives

This gives you **4 new major format categories** with only **~50MB bundle increase** and **pure Python dependencies**.

**Skip or defer**:
- RAR (requires external binary)
- TypeScript/JSX (requires large binary)
- SCSS (requires binary)
- PPT → PDF (too complex)

---

**Ready to proceed with Phase 2 Tier 1?**

**Date**: 2026-02-04  
**Status**: Planning Complete
