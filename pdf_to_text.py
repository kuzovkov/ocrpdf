#!/usr/bin/env python3
import os
import sys
import argparse
import subprocess
import requests
import base64
from pathlib import Path
from dotenv import load_dotenv

def main():
    # Load environment variables
    load_dotenv()
    
    parser = argparse.ArgumentParser(description='Convert PDF to text via LMStudio')
    parser.add_argument('input_pdf', help='Path to input PDF file')
    parser.add_argument('--skip-extraction', action='store_true',
                      help='Skip PDF to PNG conversion step')
    parser.add_argument('--page', type=str, help='Process single page by number (e.g. 001)')
    parser.add_argument('--tesseract', action='store_true',
                      help='Use tesseract OCR instead of LMStudio')
    args = parser.parse_args()

    pdf_path = Path(args.input_pdf)
    if not pdf_path.exists():
        print(f"Error: File {pdf_path} not found")
        sys.exit(1)

    base_name = pdf_path.stem
    output_dir = pdf_path.parent / base_name
    png_dir = output_dir / "pngs"
    txt_dir = output_dir / "texts"

    try:
        # Create output directories
        png_dir.mkdir(parents=True, exist_ok=True)
        txt_dir.mkdir(parents=True, exist_ok=True)

        print(f"Processing {pdf_path}...")
        
        # Step 1: Convert PDF to PNGs (if not skipped)
        if not args.skip_extraction:
            png_prefix = png_dir / f"{base_name}-page"
            subprocess.run([
                "pdftoppm",
                "-png",
                "-r", "300",
                str(pdf_path),
                str(png_prefix)
            ], check=True)
        else:
            if not any(png_dir.glob("*.png")):
                print(f"Error: No PNG files found in {png_dir}")
                sys.exit(1)

        # Step 2: Process PNG files with LMStudio
        png_files = sorted(png_dir.glob("*.png"))
        
        if args.page:
            # Process single page
            page_file = png_dir / f"{base_name}-page-{args.page}.png"
            if not page_file.exists():
                print(f"Error: Page {args.page} not found in {png_dir}")
                sys.exit(1)
                
            print(f"Processing single page: {page_file.name}...")
            txt_file = txt_dir / f"{page_file.stem}.txt"
            if args.tesseract:
                extracted_text = process_image_with_tesseract(page_file)
            else:
                extracted_text = process_image_with_lmstudio(page_file)
            with open(txt_file, "w", encoding="utf-8") as f:
                f.write(extracted_text)
        else:
            # Process all pages
            for png_file in png_files:
                print(f"Processing {png_file.name}...")
                txt_file = txt_dir / f"{png_file.stem}.txt"
                
                if args.tesseract:
                    extracted_text = process_image_with_tesseract(png_file)
                else:
                    extracted_text = process_image_with_lmstudio(png_file)
                with open(txt_file, "w", encoding="utf-8") as f:
                    f.write(extracted_text)

        print(f"Processing complete. Results saved in {output_dir}")

    except subprocess.CalledProcessError as e:
        print(f"Error during PDF conversion: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

def process_image_with_lmstudio(image_path):
    """Send image to local LMStudio API for text extraction"""
    try:
        # LMStudio typically runs on localhost:1234
        url = "http://192.168.0.118:1234/v1/chat/completions"
        
        # Read image as base64
        with open(image_path, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode("utf-8")
        
        # Get settings from environment
        model = os.getenv("LMSTUDIO_MODEL", "google/gemma-3-27b")
        system_prompt = os.getenv("LMSTUDIO_SYSTEM_PROMPT", "Распознай эту страницу и выведи только текст дословно, более ничего выводить не нужно")
        user_prompt = os.getenv("LMSTUDIO_USER_PROMPT", "Распознай эту страницу и выведи только текст дословно, более ничего выводить не нужно.")
        
        headers = {"Content-Type": "application/json"}
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{image_data}",
                                "format": "png",
                                "detail": "high"
                            }
                        },
                        {
                            "type": "text",
                            "text": user_prompt
                        }
                    ]
                }
            ],
            "temperature": 0.0,
            "max_tokens": -1,
            "stream": False
        }
        
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json()["choices"][0]["message"]["content"]
    
    except Exception as e:
        print(f"Error processing {image_path.name}: {e}")
        return ""

def process_image_with_tesseract(image_path):
    """Run tesseract OCR on image and return extracted text"""
    try:
        result = subprocess.run(
            ['tesseract', str(image_path), 'stdout', '-l', 'rus+eng', '--oem', '0'],
            capture_output=True,
            text=True,
            encoding='utf-8',
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Tesseract error: {e.stderr}")
        return ""
    except Exception as e:
        print(f"Unexpected error in tesseract: {e}")
        return ""


if __name__ == "__main__":
    main()