from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import urllib.parse

app = Flask(__name__)
app.config["DEBUG"] = True

password = 'Test@12345'

escaped_password = urllib.parse.quote_plus(password)

database_uri = f"mysql+mysqlconnector://root:{escaped_password}@localhost/laserants_LabLibros"

app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(250), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    current_price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Books {self.title}>'

@app.route('/', methods=['GET'])
def main():
    return "hola", 200

@app.route('/book', methods=['GET'])
def getEmployees():
    books = Books.query.all()
    books_list = []
    for book in books:
        book_data = {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "quantity": book.quantity,
            "current_price": book.current_price
        }
        books_list.append(book_data)
    return jsonify(books_list), 200

@app.route('/book/<id>', methods=['GET'])
def getBookById(id):
    book = Books.query.get(id)
    if book is None:
        return jsonify({"message": "book not found", "type": "NotFound"}), 404
    Book_data = {
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "quantity": book.quantity,
        "current_price": book.current_price
    }
    area = request.args.get("area")
    if area:
        Book_data["area"] = area
    return jsonify(Book_data), 200

@app.route('/book', methods=['POST'])
def createBook():
    data = request.get_json()
    new_book = Books(isbn=data['isbn'], title=data['title'],author=data['author'], quantity=data['quantity'], current_price=data['current_price'] )
    db.session.add(new_book)
    db.session.commit()
    return jsonify({"message": "Book created successfully", "book": {
        "id": new_book.id,
        "title": new_book.title,
        "author": new_book.author,
        "quantity": new_book.quantity,
        "current_price": new_book.current_price
    }}), 201

if __name__ == '__main__':
    app.run()
