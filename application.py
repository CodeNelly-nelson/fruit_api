from email.mime import application
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define Drink model
class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120))

    def to_dict(self):
        return {"id": self.id, "name": self.name, "description": self.description}

    def __repr__(self):
        return f"{self.name} - {self.description}"

# Home route
@app.route('/')
def index():
    return "Welcome to my fruit REST API"

# Get all drinks
@app.route('/drinks', methods=['GET'])
def get_drinks():
    drinks = Drink.query.all()
    return jsonify({"drinks": [drink.to_dict() for drink in drinks]})

# Get one drink by ID
@app.route('/drinks/<int:id>', methods=['GET'])
def get_drink(id):
    drink = Drink.query.get_or_404(id)
    return jsonify(drink.to_dict())

# Create a new drink
@app.route('/drinks', methods=['POST'])
def add_drink():
    if not request.json or not 'name' in request.json:
        return jsonify({'error': 'Bad Request'}), 400

    new_drink = Drink(
        name=request.json["name"],
        description=request.json.get("description", "")
    )
    db.session.add(new_drink)
    db.session.commit()
    return jsonify(new_drink.to_dict()), 201

# Delete a drink
@app.route('/drinks/<int:id>', methods=['DELETE'])
def delete_drink(id):
    drink = Drink.query.get_or_404(id)
    db.session.delete(drink)
    db.session.commit()
    return jsonify({"message": f"Drink with ID {id} deleted"}), 200

# Initialize DB if running directly
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)

