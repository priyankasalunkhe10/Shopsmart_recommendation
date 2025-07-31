from flask import Flask, jsonify, request
from database import engine, SessionLocal, Base
from routes import customer_routes
from routes import product_routes
from routes import transaction_routes
from models.customer import Customer
from recommender_utils import recommend_by_customer_id

app = Flask(__name__)

Base.metadata.create_all(bind=engine)

app.register_blueprint(customer_routes.router)
app.register_blueprint(product_routes.router)
app.register_blueprint(transaction_routes.router)

@app.route('/')
def home():
    return "Shopsmart API is running"

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    customer_id = data.get("customer_id")

    if not customer_id:
        return jsonify({"error": "customer_id is required"}), 400

    db = SessionLocal()
    customer = db.query(Customer).filter_by(customer_id=customer_id).first()
    db.close()

    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    return jsonify({
        "customer_id": customer.customer_id,
        "name": customer.name,
        "email": customer.email,
        "phone_no": customer.phone_no,
        "location": customer.location
    })

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    customer_id = data.get('customer_id')

    if not customer_id:
        return jsonify({'error': 'customer_id is required'}), 400

    try:
        customer_id = int(customer_id)
    except ValueError:
        return jsonify({'error': 'customer_id must be an integer'}), 400

    recommendations = recommend_by_customer_id(customer_id)
    if not recommendations:
        return jsonify({'message': 'No recommendations found'}), 404

    return jsonify({'recommendations': recommendations})

if __name__ == '__main__':
    app.run(debug=True)
