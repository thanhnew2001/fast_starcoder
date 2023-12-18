from flask import Flask, request, jsonify
from hf_hub_ctranslate2 import GeneratorCT2fromHfHub

import ctranslate2
import transformers

model_name = "envit-ct2"
translator = ctranslate2.Translator(model_name)
tokenizer = transformers.AutoTokenizer.from_pretrained(model_name)

def translate(text):
  input_text = f"""translate English to Vietnamese: {text}"""
  input_tokens = tokenizer.convert_ids_to_tokens(tokenizer.encode(input_text))
  
  results = translator.translate_batch([input_tokens])
  
  output_tokens = results[0].hypotheses[0]
  output_text = tokenizer.decode(tokenizer.convert_tokens_to_ids(output_tokens))
  return output_text


app = Flask(__name__)

@app.route('/translate', methods=['POST'])
def translate_api():
  try:
    data = request.get_json()
    text = data['text']
    target = data['target']
    
    translated = translate(text)
    
    return jsonify({'translation': translated})

  except Exception as e:
    return jsonify({"error": str(e)})

if __name__ == '__main__':
  app.run(host='0.0.0.0')
