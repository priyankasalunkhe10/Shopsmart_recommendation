from flask import Flask,jsonify,request
import pickle
import pandas as pd
from database import Base,engine
from routes import customer_routes
from routes import product_routes
from routes import transaction_routes

import models.customer
import models.product
import models.transaction

with open('ML_model/location_product_counts.pkl', 'rb') as f:
    location_product_counts = pickle.load(f)

app=Flask(__name__)

Base.metadata.create_all(bind=engine)

app.register_blueprint(customer_routes.router)
app.register_blueprint(product_routes.router)
app.register_blueprint(transaction_routes.router)

@app.route('/')
def home():
    return "Shopsmart API is running"

def recommend_products_by_location(location, top_n=5):
    filtered = location_product_counts[location_product_counts['location'].str.lower() == location.lower()]
    filtered = filtered.sort_values(by='purchase_count', ascending=False)
    return filtered[['product_id', 'name']].head(top_n).to_dict(orient='records')

@app.route('/recommend/<string:location>', methods=['GET'])
def recommend(location):
    
    if not location:
        return jsonify({'error': 'Location not provided'}), 400

    recommendations = recommend_products_by_location(location)

    if not recommendations:
        return jsonify({'message': f'No recommendations found for location: {location}'}), 404

    return jsonify({'location': location, 'recommendations': recommendations})

if __name__=='__main__':
    app.run(debug=True)