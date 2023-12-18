from flask import Flask, request, jsonify
import ctranslate2
import transformers

model_name = "envit-ct2"
translator = ctranslate2.Translator(model_name)
tokenizer = transformers.AutoTokenizer.from_pretrained(model_name)

def translate(texts):
    input_texts = [f"translate English to Vietnamese: {text}" for text in texts]
    input_tokens = [tokenizer.encode(text, add_special_tokens=True) for text in input_texts]
    
    results = translator.translate_batch(input_tokens)
    
    output_texts = []
    for result in results:
        output_tokens = result[0]["tokens"]
        output_text = tokenizer.decode(output_tokens, skip_special_tokens=True)
        output_texts.append(output_text)
    
    return output_texts

app = Flask(__name__)

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
