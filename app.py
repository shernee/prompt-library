from flask import Flask, render_template, request, redirect, url_for, jsonify
import pinecone
import os
import openai

app = Flask(__name__)

def generate_embedding(prompt):
    openai.api_key = os.environ["OPENAI_API_KEY"]
    prompt_vector = openai.Embedding.create(
        input=prompt,
        model="text-embedding-ada-002"
    )["data"][0]["embedding"]
    return prompt_vector

@app.route("/")
def hello_world():
    return render_template('home.html')


@app.route("/search-results", methods=["POST"])
def search_results():
    user_prompt = request.form.get('user_prompt')
    print(user_prompt)
    if user_prompt:
        pinecone.init(api_key=os.environ["PINECONE_API_KEY"], environment="gcp-starter")
        # pinecone.delete_index("prompt-library")
        # pinecone.create_index("prompt-library", dimension=1536, metric="euclidean")
        index = pinecone.Index(index_name="prompt-library")
        embedding = generate_embedding(user_prompt)
        response_vector = index.query(
            vector=embedding,
            filter={"prompttype": "instruction"}, 
            top_k=3
        )
        print(response_vector)
        if response_vector:
            response = response_vector
        else:
            response = "No matching response found."
        # indexes = pinecone.list_indexes()

        return jsonify({"response": response})
    else:
        return jsonify({"response": "Please provide a user prompt."})
    
@app.route("/add-prompt", methods=["POST"])
def add_prompt():
    prompt = request.form.get('prompt')
    prompttype = request.form.get('prompttype')
    domain = request.form.get('domain')
    if prompt:
        embedding = generate_embedding(prompt)

        pinecone.init(api_key=os.environ["PINECONE_API_KEY"], environment="gcp-starter")
        index = pinecone.Index(index_name="prompt-library")
        metadata = {"prompttype": prompttype, "domain": domain}
        pinecone_vector = (prompt, embedding, metadata)
        upsert_count = index.upsert(vectors=[pinecone_vector])['upserted_count']
        index_stats = index.describe_index_stats()
        response = f"Your prompt has been added! Total prompt count {index_stats['total_vector_count']}"
        if upsert_count:
            return jsonify({"response": response})
    else:
        return jsonify({"response": "Please provide a user prompt."})
    

