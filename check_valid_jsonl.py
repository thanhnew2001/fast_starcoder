import json

def is_valid_jsonl(file_path):
    """
    Checks if a file is a valid JSONL file and prints all invalid lines.
    Returns True if all lines are valid JSON objects, False otherwise.
    """
    is_valid = True
    invalid_lines = []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, start=1):
                try:
                    json.loads(line)  # Attempt to parse the JSON line
                except json.JSONDecodeError:
                    invalid_lines.append(line_num)
                    is_valid = False

        if not is_valid:
            print(f"The file {file_path} has invalid JSONL lines: {invalid_lines}")
        return is_valid

    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

# Example usage
jsonl_file_path = 'output.jsonl'
if is_valid_jsonl(jsonl_file_path):
    print(f"The file {jsonl_file_path} is a valid JSONL file.")
else:
    print(f"The file {jsonl_file_path} is not a valid JSONL file.")

