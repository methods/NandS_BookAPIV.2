from flask import Flask, request, jsonify
from data import books

app = Flask(__name__)

@app.route("/helloworld")
def helloworld():
    return "hello world"

@app.route("/books", methods=["POST"])
def add_book():
    try:
        new_book = request.json

        books.append(new_book)
        return jsonify(books[-1]), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)