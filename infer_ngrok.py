import os
import threading

from flask import Flask
from pyngrok import ngrok
from hf_hub_ctranslate2 import GeneratorCT2fromHfHub

from flask import request, jsonify

model_name = "michaelfeil/ct2fast-starcoder"
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

@app.route('/generate_code', methods=['GET'])
def generate_code():
    try:
        # Get the list of prompts from the query string parameter 'prompts'
        prompts = request.args.getlist('prompts')
        return generate_text_batch(prompts)

    except Exception as e:
        return jsonify({"error": str(e)})

# Start the Flask server in a new thread
threading.Thread(target=app.run, kwargs={"use_reloader": False}).start()
