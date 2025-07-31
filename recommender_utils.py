import pandas as pd
from sqlalchemy.orm import Session
from database import engine
from models.customer import Customer
from models.product import Product
from models.transaction import Transaction

# Function to recommend top N products based on customer's location
def recommend_by_customer_id(customer_id: int, top_n: int = 5):
    session = Session(bind=engine)

    try:
        customer = session.query(Customer).filter_by(customer_id=customer_id).first()
        if not customer:
            return []

        location = customer.location

        # Get all customers in the same location
        same_location_customers = session.query(Customer.customer_id).filter_by(location=location).all()
        same_location_customers = [c.customer_id for c in same_location_customers]

        # Get transactions and join with products
        transactions = session.query(Transaction).all()
        products = session.query(Product).all()

        df_transactions = pd.DataFrame([{
            'transaction_id': t.transaction_id,
            'customer_id': t.customer_id,
            'product_id': t.product_id,
            'purchase_date': t.purchase_date
        } for t in transactions])

        df_products = pd.DataFrame([{
            'product_id': p.product_id,
            'name': p.name,
            'category': p.category
        } for p in products])

        if df_transactions.empty or df_products.empty:
            return []

        # Filter transactions for customers in the same location
        local_transactions = df_transactions[df_transactions['customer_id'].isin(same_location_customers)]
        merged_df = pd.merge(local_transactions, df_products, on='product_id', how='left')

        if merged_df.empty:
            return []

        top_products = (
            merged_df.groupby(['product_id', 'name'])
            .size()
            .reset_index(name='purchase_count')
            .sort_values(by='purchase_count', ascending=False)
            .head(top_n)
        )

        return top_products.to_dict(orient='records')

    finally:
        session.close()


def save_customer(data: dict):
    session = Session(bind=engine)
    try:
        customer = Customer(**data)
        session.add(customer)
        session.commit()
        return True
    except Exception as e:
        print("Error saving customer:", e)
        session.rollback()
        return False
    finally:
        session.close()
