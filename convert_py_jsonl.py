import os
import json

def process_file(file_path):
    """
    Reads the contents of a file, trying different encodings in case of a UnicodeDecodeError.
    Removes lines that are likely to contain copyright information.
    Returns a single string with newline characters replaced by spaces.
    """
    encodings = ['utf-8', 'ISO-8859-1', 'Windows-1252']
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                lines = file.readlines()

            # Filter out copyright lines
            filtered_lines = [line for line in lines if not is_copyright_line(line)]

            return ' '.join(filtered_lines).replace('\n', ' ')
        except UnicodeDecodeError:
            continue
    return ""  # Return empty string if all encodings fail

def is_copyright_line(line):
    """
    Checks if a line of text is likely to contain copyright information.
    """
    line = line.lower()
    keywords = ['copyright', 'all rights reserved', '©', '(c)']
    return any(keyword in line for keyword in keywords)

def is_valid_file(file_name):
    """
    Checks if the file is a .py or .md file and not a readme.md.
    """
    return (file_name.endswith('.py') or 
            (file_name.endswith('.py') and not file_name.lower() == 'readme.md'))

import os
import json


def process_directory(directory, output_file):
    """
    Processes each file in the directory and its subdirectories,
    and writes the content and file path to the output JSONL file.
    """
    with open(output_file, 'w', encoding='utf-8') as jsonl_file:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if is_valid_file(file):
                    file_path = os.path.join(root, file)
                    file_content = process_file(file_path)
                    file_relative_path = os.path.relpath(file_path, directory)
                    json_record = {
                        "text": file_content,
                        #"file_path": file_relative_path
                    }
                    jsonl_file.write(json.dumps(json_record) + '\n')

# Directory containing the repositories
source_directory = 'taipy_repos'
# Output JSONL file
output_jsonl = 'output.jsonl'

process_directory(source_directory, output_jsonl)
print(f"Processed files from {source_directory} into {output_jsonl}")

