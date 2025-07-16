import pandas as pd
from datetime import datetime
from database import SessionLocal
from models.customer import Customer
from models.product import Product
from models.transaction import Transaction

db = SessionLocal()

df_customers = pd.read_csv('csv_files/customers.csv')
for _,row in df_customers.iterrows():
    customer = Customer(
        customer_id=row['customer_id'],
        name=row['name'],
        email=row['email'],
        phone_no=row['phone_no'],
        location=row['location']
    )
    db.merge(customer)
db.commit()

df_product = pd.read_csv('csv_files/products.csv')
for index,row in df_product.iterrows():
    product = Product(
        product_id=row['product_id'],
        name=row['name'],
        category=row['category'],
        price=row['price']
    )
    db.merge(product)
db.commit()

df_product = pd.read_csv('csv_files/transactions.csv')
for _,row in df_product.iterrows():
    transaction = Transaction(
        transaction_id=row['transaction_id'],
        customer_id=row['customer_id'],
        product_id=row['product_id'],
        purchase_date=datetime.strptime(row['purchase_date'], "%Y-%m-%d").date()
    )
    db.merge(transaction)
db.commit()

db.close()
print("successfully imported....")