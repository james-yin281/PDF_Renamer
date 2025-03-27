# PDF Renamer

## Overview
PDF Renamer is a tool designed to rename PDF files based on their metadata. It uses a language model to extract metadata such as author(s), year, journal, and title from the content of the PDF and generates a formatted filename. The tool supports renaming individual PDF files or all PDF files in a folder.

## Features
- Extracts metadata from PDF files using a language model.
- Renames PDF files based on a specific naming convention:
- Handles missing metadata by using placeholders like "Unknown."
- Supports batch renaming of PDF files in a folder.
- Reads API key and model configuration from a `config.yml` file.

## File Structure
- **`single_pdf_rename.py`**: Handles renaming of a single PDF file.
- **`folder_pdf_rename.py`**: Handles batch renaming of PDF files in a folder.
- **`config.yml`**: Stores API key and model configuration.
- **`Readme.md`**: Documentation for the project.
- **`requirements.txt`**: Contains the Python dependencies required by the project.

## Dependencies
- `PyPDF2`: For extracting text from PDF files.
- `openai`: For interacting with the language model API.
- `yaml`: For reading configuration files.
- `requests`: For making HTTP requests.

## Installation
1. Clone the repository:
```bash
git clone <repository-url>
cd PDF_Renamer
2. Install the required Python packages:
```bash
pip install -r requirements.txt
