from flask import Flask, request, jsonify
from flask_cors import CORS
from rag import ask_rag
import os

app = Flask(__name__)
CORS(app)

@app.route("/chat", methods=["POST"])
def chat():
    question = request.json.get("question")
    answer = ask_rag(question)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
