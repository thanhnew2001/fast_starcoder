from flask import Flask, request, jsonify
from hf_hub_ctranslate2 import GeneratorCT2fromHfHub

model_name = "michaelfeil/ct2fast-starcoder"
model = GeneratorCT2fromHfHub(
        # load in int8 on CUDA
        model_name_or_path=model_name,
        device="cuda",
        compute_type="int8_float16",
        # tokenizer=AutoTokenizer.from_pretrained("{ORG}/{NAME}")
)

app = Flask(__name__)

def generate_text_batch(prompt_texts, max_length=64):
    outputs = model.generate(prompt_texts, max_length=max_length, include_prompt_in_result=True)
    return outputs


@app.route('/generate_code', methods=['GET'])
def generate_code():
    try:
        # Get the list of prompts from the query string parameter 'prompts'
        prompts = request.args.getlist('prompts')
        return generate_text_batch(prompts)

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
