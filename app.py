from flask import Flask, request, jsonify
from data import books
import uuid

app = Flask(__name__)

@app.route("/helloworld")
def helloworld():
    return "hello world"

@app.route("/books", methods=["POST"])
def add_book():
    try:
        new_book = request.json
        # create UUID and add it to the new_book object
        new_book_id = str(uuid.uuid4())
        new_book["id"] = new_book_id

        # validation
        required_fields = ["title", "synopsis", "author"]
        for field in required_fields:
            if field not in new_book:
                return {"error": "Missing required fields"}, 400


        # # add a links field if there isn't one already
        # if 'links' not in new_book:
        #     new_book['links'] = {}

        # update the links with the newly generated id
        new_book['links']['self'] = f'/books/{new_book_id}'
        new_book['links']['reservations'] = f'/books/{new_book_id}/reservations'
        new_book['links']['reviews'] = f'/books/{new_book_id}/reviews'

        books.append(new_book)

        return jsonify(books[-1]), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)