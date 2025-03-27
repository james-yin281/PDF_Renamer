"""
Module for renaming PDF files in a folder using rename_pdf from single_pdf_rename.
Reads API and model information from config.yml.
"""

import os
import re
import yaml
from single_pdf_rename import rename_pdf

config = yaml.safe_load(open('config.yml'))
api_key = config['api_key']
model = config['model']

def wrap_rename_pdf(pdf_file):
    """
    Rename a PDF file using the rename_pdf function.

    Args:
        pdf_file (str): Path to the PDF file.

    Returns:
        str: The new name of the PDF file.
    """
    return rename_pdf(pdf_file, api_key, model)

def check_and_rename_pdfs(folder_path):
    """
    Check and rename PDF files in a folder if they do not match a specified pattern.

    Args:
        folder_path (str): Path to the folder containing PDF files.
    """
    pattern = re.compile(r'^\d{4}[^_]+_[^_]+_.*\.pdf$')
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".pdf"):
            if not pattern.match(filename):
                wrap_rename_pdf(os.path.join(folder_path, filename))

if __name__ == "__main__":
    folder_path = "/Users/james/Desktop/Sync/Usage/论文/News"
    check_and_rename_pdfs(folder_path)