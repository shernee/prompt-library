from flask import Flask, render_template, request, redirect, url_for, jsonify
import pinecone
import os

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('home.html')

@app.route("/search_results", methods=["POST"])
def search_results():
    user_prompt = request.form.get('user_prompt')
    print(user_prompt)
    if user_prompt:
        pinecone.init(api_key=os.environ["PINECONE_API_KEY"], environment="gcp-starter")
        pinecone.create_index("prompt-library", dimension=8, metric="euclidean")
        pinecone.describe_index("prompt-library")
        # index = pinecone.Index(index_name="prompt_library")

        # response_vector = index.query(queries=[user_prompt], top_k=1)

        # if response_vector and response_vector[0]['score'] > 0.7:
        #     response = response_vector[0]['id']
        # else:
        #     response = "No matching response found."
        indexes = pinecone.list_indexes()

        return jsonify({"response": indexes})
    else:
        return jsonify({"response": "Please provide a user prompt."})

@app.route("/test_api", methods=["POST"])
def test_api():
    user_prompt = request.form.get('user_prompt')
    print(user_prompt)

    pinecone.init(api_key=os.environ["PINECONE_API_KEY"])
