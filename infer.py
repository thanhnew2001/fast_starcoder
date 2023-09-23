model_name = "michaelfeil/ct2fast-starcoder"
from hf_hub_ctranslate2 import GeneratorCT2fromHfHub
model = GeneratorCT2fromHfHub(
        # load in int8 on CUDA
        model_name_or_path=model_name,
        device="cuda",
        compute_type="int8_float16",
        # tokenizer=AutoTokenizer.from_pretrained("{ORG}/{NAME}")
)

def generate_text_batch(prompt_texts, max_length=64):
    outputs = model.generate(prompt_texts, max_length=max_length, include_prompt_in_result=True)
    return outputs

# Example usage of the function
code_prompts = [
    "def sum(a,b,c)",
    "def reverse(string)",
    "Write a Python function to calculate the factorial of a given number.",
    "Define a Python class for a simple calculator with methods for addition, subtraction, multiplication, and division.",
    "Write a Python program that reads a CSV file, performs data analysis, and plots a line graph of the results.",
    "Write a Python program to implement the binary search algorithm on a sorted list.",
    "Create a Python function that converts a decimal number to its binary representation.",
    "Write a Python script to download files from a list of URLs.",
    "Generate Python code to sort a list of integers using the bubble sort algorithm.",
    "Write a Python program to find the largest and smallest elements in a list.",
    "Create a Python function to check if a given string is a valid email address.",
    "Write a Python program to calculate the area of a triangle given its base and height."
]

generated_texts = generate_text_batch(code_prompts, 100)

for text in generated_texts:
    print(text)
