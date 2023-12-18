from flask import Flask, request, jsonify
import ctranslate2
import transformers

model_name = "envit-ct2"
translator = ctranslate2.Translator(model_name)
tokenizer = transformers.AutoTokenizer.from_pretrained(model_name)

def translate(texts):
    input_tokens_list = []
    for text in texts:
        encoded = tokenizer.encode(text)
        tokens = tokenizer.convert_ids_to_tokens(encoded)
        input_tokens_list.append(tokens)

    # Call translate_batch with the list of tokenized texts
    # results = translator.translate_batch(tokenized_texts, batch_type='tokens', max_batch_size=50)
    results = translator.translate_batch(input_tokens_list)
    output_text_list = []
    for result in results:
        output_tokens = result.hypotheses[0]
        output_text = tokenizer.decode(tokenizer.convert_tokens_to_ids(output_tokens))
        print(output_text)    
        output_text_list.append(output_text)
    return output_text_list
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
