import os
import requests
import PyPDF2
import json
import argparse
import openai
import yaml
from openai import OpenAI

def extract_text_from_pdf(pdf_path):
    """
    Extract text from the first few pages of a PDF.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        str: Text extracted from the PDF.
    """
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        max_pages = min(5, len(reader.pages))
        for page_num in range(max_pages):
            text += reader.pages[page_num].extract_text()
    return text

def call_llm_api(pdf_text, api_key, model):
    """
    Call Ali's LLM API to generate a new filename from extracted text.

    Args:
        pdf_text (str): Text extracted from the PDF.
        api_key (str): API key for authentication.
        model (str): Model name for the LLM.

    Returns:
        str: Generated filename based on the extracted metadata.
    """
    client = OpenAI(
        api_key=api_key,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
    )

    reasoning_content = ""
    answer_content = ""
    is_answering = False

    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that extracts paper metadata from text and outputs a formatted filename."},
            {"role": "user", "content": (
                f"Extract metadata from the provided text below:\n\n"
                f"- Author(s)\n"
                f"- Year\n"
                f"- Journal\n"
                f"- Title\n\n"
                f"Using the extracted metadata, create a filename in this exact format:\n"
                f"'year[short name for journal or WP for workingpaper]_[author]_title.pdf'\n\n"
                f"Note:\n"
                f"- If any information is missing, use 'Unknown' as a placeholder.\n"
                f"- The short name for journal (or WP) and author must be enclosed within square brackets ([]).\n"
                f"- If there are exactly two authors, connect them with 'and'. If there are more than two, list only the first author followed by 'et al.'.\n"
                f"- Output only the filename, and nothing else.\n\n"
                f"Text:\n{pdf_text}"
            )}
        ],
        max_tokens=400,
        stream=True
    )

    for chunk in completion:
        if chunk.choices:
            delta = chunk.choices[0].delta
            if hasattr(delta, 'reasoning_content') and delta.reasoning_content is not None:
                reasoning_content += delta.reasoning_content
            else:
                if delta.content != "" and is_answering is False:
                    is_answering = True
                answer_content += delta.content

    response = {"choices": [{"message": {"content": answer_content}}]}
    return response["choices"][0]["message"]["content"]

def rename_pdf(pdf_path, api_key, model):
    """
    Extract text from a PDF, call the LLM API, and rename the file.

    Args:
        pdf_path (str): Path to the PDF file.
        api_key (str): API key for LLM authentication.
        model (str): Model name for the LLM.

    Returns:
        str: New path of the renamed PDF.
    """
    pdf_text = extract_text_from_pdf(pdf_path)
    new_filename = call_llm_api(pdf_text, api_key, model)
    dir_path = os.path.dirname(os.path.abspath(pdf_path))
    new_path = os.path.join(dir_path, new_filename)

    os.rename(pdf_path, new_path)
    print(f"Renamed PDF to: {new_filename}")
    return new_path

if __name__ == "__main__":
    with open('config.yml', "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    api_key = data['api_key']
    model = data['model']
    rename_pdf("/Users/james/Desktop/Sync/Usage/论文/News/SSRN-id2667658.pdf", api_key, model)
