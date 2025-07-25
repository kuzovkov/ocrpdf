# PDF to Text Converter

This tool converts PDF files containing scanned pages into text using OCR via LMStudio or Tesseract.

## Requirements
- Python 3.6+
- pdftoppm (part of Poppler utilities)
- LMStudio running locally on port 1234 OR
- Tesseract OCR (for --tesseract option)

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

3. Install Tesseract OCR (if using --tesseract option):
  ```bash
  # Ubuntu/Debian
  sudo apt install tesseract-ocr tesseract-ocr-rus

  # Or install with snap
  sudo snap install tesseract
sudo snap list
...
tesseract               5.4.1+pkg-944a                   2507   latest/stable  brlin        
...

/snap/bin/tesseract --version
tesseract 5.4.1
 leptonica-1.84.1
  libjpeg 8d (libjpeg-turbo 2.1.2) : libpng 1.6.37 : libtiff 4.3.0 : zlib 1.2.11 : libwebp 1.2.2 : libopenjp2 2.4.0
 Found AVX2
 Found AVX
 Found FMA
 Found SSE4.1
 Found OpenMP 201511
 Found libarchive 3.6.0 zlib/1.2.11 liblzma/5.2.5 bz2lib/1.0.8 liblz4/1.9.3 libzstd/1.4.8
 Found libcurl/7.81.0 GnuTLS/3.7.3 zlib/1.2.11 brotli/1.0.9 zstd/1.4.8 libidn2/2.3.2 libpsl/0.21.0 (+libidn2/2.3.2) libssh/0.9.6/openssl/zlib nghttp2/1.43.0 librtmp/2.3 OpenLDAP/2.5.18

snap/bin/tesseract --list-langs
List of available languages in "/snap/tesseract/current/usr/local/share/tessdata/" (0):

mkdir -p ~/tessdata
cd ~/tessdata
wget https://github.com/tesseract-ocr/tessdata/raw/main/rus.traineddata
wget https://github.com/tesseract-ocr/tessdata/raw/main/eng.traineddata

nano .bashrc
add line:
export TESSDATA_PREFIX=~/tessdata
export PATH=$PATH:/snap/bin # if need
----------------
source ~/.bashrc
 
tesseract --oem 0 --list-langs
eng
rus

  # macOS (using Homebrew)
  brew install tesseract
  ```
 

## Usage

### Basic Conversion
```bash
python pdf_to_text.py input.pdf
```

### Advanced Options
```bash
python pdf_to_text.py input.pdf --skip-extraction --page 001 --tesseract
```
- `--skip-extraction` - Skip PDF to PNG conversion step (requires existing PNG files in `input-name/pngs/`)
- `--page` - Send to recognize only predefined page number, for example 001 (requires existing PNG file in `input-name/pngs/`)
- `--tesseract` - Use Tesseract OCR instead of LMStudio (requires Tesseract installed)

The tool will:
1. Create a directory named after the input file (without extension)
2. Extract PDF pages as PNG images in `input-name/pngs/` (unless skipped)
3. Process each PNG through LMStudio or Tesseract to extract text
4. Save extracted text to `input-name/texts/` as .txt files

## Notes
- For LMStudio: ensure it's running with a vision-capable model before processing
- For Tesseract: install language packs for required languages (rus+eng)
- Processing time depends on PDF size and OCR engine performance


## Merge text files into one
```bash
#example
ls texts/Том-2-page-*.txt | sort -V | xargs cat > texts/Том-2.txt
find texts -type f -name 'Том-2-page-*.txt' | sort -V | xargs -d '\n' cat > texts/Том-2.txt
```

