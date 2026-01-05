from flask import Flask, request, jsonify
from flask_cors import CORS
from rag import ask_rag

app = Flask(__name__)
CORS(app)

@app.route("/chat", methods=["POST"])
def chat():
    question = request.json.get("question")
    answer = ask_rag(question)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(port=8000)
