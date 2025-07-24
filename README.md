# PDF to Text Converter

This tool converts PDF files containing scanned pages into text using OCR via LMStudio.

## Requirements
- Python 3.6+
- pdftoppm (part of Poppler utilities)
- LMStudio running locally on port 1234

## Installation
1. Install Poppler utilities:
   ```bash
   # Ubuntu/Debian
   sudo apt install poppler-utils
   
   # macOS (using Homebrew)
   brew install poppler
   ```

2. Install Python dependencies:
   ```bash
   pip install requests
   ```

## Usage

### Basic Conversion
```bash
python pdf_to_text.py input.pdf
```

### Advanced Options
```bash
python pdf_to_text.py input.pdf --skip-extraction
```
- `--skip-extraction` - Skip PDF to PNG conversion step (requires existing PNG files in `input-name/pngs/`)

The tool will:
1. Create a directory named after the input file (without extension)
2. Extract PDF pages as PNG images in `input-name/pngs/` (unless skipped)
3. Process each PNG through LMStudio to extract text
4. Save extracted text to `input-name/texts/` as .txt files

## Notes
- Ensure LMStudio is running with a vision-capable model before processing
- Processing time depends on PDF size and LMStudio performance