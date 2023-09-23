from flask import Flask, request, jsonify
import requests
import threading
import time
import random
from pyngrok import ngrok

app = Flask(__name__)
port = "4000"

# Open a ngrok tunnel to the HTTP server
public_url = ngrok.connect(port).public_url
print(" * ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}\"".format(public_url, port))

# Update any base URLs to use the public ngrok URL
app.config["BASE_URL"] = public_url

# Store incoming prompts in a queue with unique IDs
prompt_queue = []

# Lock for thread synchronization
prompt_lock = threading.Lock()

# Store the results of batch processing
batch_results = []

# Maximum time window for batch processing (in seconds)
BATCH_WINDOW_SECONDS = 2

def process_batch():
    global prompt_queue, batch_results
    while True:
        time.sleep(BATCH_WINDOW_SECONDS)
        with prompt_lock:
            if prompt_queue:
                batch_prompts = prompt_queue.copy()
                prompt_queue = []
                batch_results = []  # Clear previous results

                # Assign unique IDs to prompts and create a dictionary to store them
                id_ = random.randint(100000, 999999)
              
                # Call the external API with the batch of prompts
                # external_api_url = "https://139a-213-224-31-105.ngrok-free.app/generate_code?max_length=128&"
                # prompts_query = "&".join([f"prompts=#id_{id_}:{prompt['prompt']}" for prompt in batch_prompts])
                # response = requests.get(external_api_url + prompts_query)
                
                batch_results = ["response1", "response2", "response3"]
                # Update batch_results with the responses from the external API
                if response.status_code == 200:
                    response_data = response.json()
                    batch_results = response_data

# Start the batch processing thread
batch_thread = threading.Thread(target=process_batch)
batch_thread.start()

@app.route('/batch_prompt', methods=['GET'])
def batch_prompt():
    try:
        prompts = request.args.getlist('prompts', type=str)
        with prompt_lock:
            prompt_queue.extend(prompts)
        return jsonify({"message": "Prompts added to batch processing queue."}), 202
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/get_batch_results', methods=['GET'])
def get_batch_results():
    global batch_results
    with prompt_lock:
        results = batch_results.copy()
    return results

if __name__ == '__main__':
    app.run(debug=True)
