from flask import Flask, request, jsonify
from hf_hub_ctranslate2 import GeneratorCT2fromHfHub

model = GeneratorCT2fromHfHub("envit-ct2") 

app = Flask(__name__)

@app.route('/translate', methods=['POST'])
def translate():
  try:
    data = request.get_json()
    text = data['text']
    target = data['target']
    
    translated = model.generate([text], target_language=target)[0]
    
    return jsonify({'translation': translated})

  except Exception as e:
    return jsonify({"error": str(e)})

if __name__ == '__main__':
  app.run(host='0.0.0.0')
