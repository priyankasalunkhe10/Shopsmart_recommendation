from flask import Flask
from database import Base,engine
from routes import customer_routes
from routes import product_routes
from routes import transaction_routes

import models.customer
import models.product
import models.transaction

app=Flask(__name__)

Base.metadata.create_all(bind=engine)

app.register_blueprint(customer_routes.router)
app.register_blueprint(product_routes.router)
app.register_blueprint(transaction_routes.router)

@app.route('/')
def home():
    return "Shopsmart API is running"

if __name__=='__main__':
    app.run(debug=True)