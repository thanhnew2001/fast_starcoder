from flask import Flask, request, jsonify
import ctranslate2
import transformers

# Initialize the translator and tokenizer
model_name = "envit-ct2"
translator = ctranslate2.Translator(model_name)
tokenizer = transformers.AutoTokenizer.from_pretrained(model_name)

# Function to perform batch translation
def translate(texts):
    # Encode each text to get token IDs
    input_ids_list = [tokenizer.encode(f"translate English to German: {text}", add_special_tokens=True) for text in texts]

    # Call translate_batch with the list of token IDs
    results = translator.translate_batch(input_ids_list)

    # Process results to obtain output texts
    output_texts = []
    for result in results:
        output_tokens = result[0]['hypotheses'][0]
        output_ids = tokenizer.convert_tokens_to_ids(output_tokens)
        output_text = tokenizer.decode(output_ids, skip_special_tokens=True)
        output_texts.append(output_text)
    
    return output_texts

app = Flask(__name__)

# Define the Flask route for translation
@app.route('/translate', methods=['POST'])
def translate_api():
    try:
        data = request.get_json()
        texts = data['texts']  # Expecting a list of texts

        if not isinstance(texts, list):
            raise ValueError("Input 'texts' must be a list of strings.")
        
        translations = translate(texts)
        
        return jsonify({'translations': translations})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0')
