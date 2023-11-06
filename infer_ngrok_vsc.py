import os
import threading

from flask import Flask
from pyngrok import ngrok
from hf_hub_ctranslate2 import GeneratorCT2fromHfHub

from flask import request, jsonify

model_name = "michaelfeil/ct2fast-starcoderbase-3b"
#model_name = "michaelfeil/ct2fast-starchat-alpha"
#model_name = "michaelfeil/ct2fast-starchat-beta"
model = GeneratorCT2fromHfHub(
        # load in int8 on CUDA
        model_name_or_path=model_name,
        device="cuda",
        compute_type="int8_float16",
        # tokenizer=AutoTokenizer.from_pretrained("{ORG}/{NAME}")
)

def generate_text_batch(prompt_texts, max_length=64):
    outputs = model.generate(prompt_texts, max_length=max_length, include_prompt_in_result=False)
    return outputs

app = Flask(__name__)
port = "5000"

# Open a ngrok tunnel to the HTTP server
public_url = ngrok.connect(port).public_url
print(" * ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}\"".format(public_url, port))

# Update any base URLs to use the public ngrok URL
app.config["BASE_URL"] = public_url

# ... Update inbound traffic via APIs to use the public-facing ngrok URL
# Define Flask routes
@app.route("/")
def index():
    return "Hello from Colab!"

@app.route("/api/generate/", methods=["POST"])
def generate_code():
    try:
        # Get the JSON data from the request body
        data = request.get_json()
        
        # Extract 'inputs' and 'parameters' from the JSON data
        inputs = data.get('inputs', "")
        parameters = data.get('parameters', {})
        
        # Extract the 'max_new_tokens' parameter
        max_new_tokens = parameters.get('max_new_tokens', 64)

        # Call the generate_text_batch function with inputs and max_new_tokens
        generated_text = generate_text_batch([inputs], max_new_tokens)[0]

        return jsonify({
        "generated_text": generated_text,
        "status": 200
        })

    except Exception as e:
        return jsonify({"error": str(e)})


# Start the Flask server in a new thread
threading.Thread(target=app.run, kwargs={"use_reloader": False}).start()
