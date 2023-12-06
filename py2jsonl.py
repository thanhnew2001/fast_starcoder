import os
import json

def tokenize_code(code, max_characters=256):
    """
    Tokenize code into snippets of specified max_characters, breaking at new lines.
    """
    lines = code.split('\n')
    snippets = []
    current_snippet = ""

    for line in lines:
        if len(current_snippet) + len(line) + 1 <= max_characters:
            current_snippet += line + '\n'
        else:
            snippets.append(current_snippet.strip())
            current_snippet = line + '\n'

    if current_snippet:
        snippets.append(current_snippet.strip())

    return snippets

def process_file(file_path):
    """
    Read a file, tokenize the code, and create snippets.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Tokenize code into snippets of 128 characters at new lines
    snippets = tokenize_code(content)

    return snippets

def escape_string(s):
    """
    Do not escape triple quotes, double quotes, single quotes, and new lines.
    """
    return s

def main(input_folder, output_file):
    snippets_list = []

    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith(('.py', '.md')):
                file_path = os.path.join(root, file)
                snippets = process_file(file_path)
                for snippet in snippets:
                    escaped_snippet = escape_string(snippet)
                    snippets_list.append({'text': escaped_snippet})

    # Write snippets to a JSONL file
    with open(output_file, 'w', encoding='utf-8') as jsonl_file:
        for snippet in snippets_list:
            jsonl_file.write(json.dumps(snippet) + '\n')

if __name__ == "__main__":
    input_folder = 'taipy'  # replace with your folder path
    output_file = 'snippets.jsonl'  # replace with your desired output file path
    main(input_folder, output_file)
