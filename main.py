from flask import Flask
from database import Base,engine
from routes import customer_routes
from routes import product_routes
from routes import transaction_routes

import models.customer
import models.product
import models.transaction

from routes.recommend_routes import get_recommend_blueprint

app=Flask(__name__)

import pickle

with open('ML_model/recommendation_model.pkl', 'rb') as f:
    model_data = pickle.load(f)

knn_location = model_data['knn_location']
knn_purchase = model_data['knn_purchase']
similarity_matrix = model_data['similarity_matrix']
location_vectorizer = model_data['location_vectorizer']
product_vectorizer = model_data['product_vectorizer']
user_item_matrix = model_data['user_item_matrix']
df_product = model_data['df_product']
df_customer = model_data['df_customer']
df_transaction = model_data['df_transaction']

recommend_bp = get_recommend_blueprint(
    knn_location, knn_purchase, similarity_matrix,
    location_vectorizer, product_vectorizer,
    user_item_matrix, df_product, df_customer, df_transaction
)

Base.metadata.create_all(bind=engine)

app.register_blueprint(customer_routes.router)
app.register_blueprint(product_routes.router)
app.register_blueprint(transaction_routes.router)
app.register_blueprint(recommend_bp)

@app.route('/')
def home():
    return "Shopsmart API is running"

if __name__=='__main__':
    app.run(debug=True)