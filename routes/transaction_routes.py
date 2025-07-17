from flask import Blueprint, request, jsonify
from database import SessionLocal
from models.transaction import Transaction

router = Blueprint('transactions', __name__)

@router.route('/transactions',methods=['POST'])
def add_transaction():
    db=SessionLocal()
    data=request.json
    transaction = Transaction(customer_id = data.get('customer_id'),
                        product_id = data.get('product_id'),
                        purchase_date = data.get('purchase_date'))
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    db.close()
    return jsonify({"transaction_id":transaction.transaction_id})

@router.route('/transactions',methods = ['GET'])
def get_all():
    db = SessionLocal()
    transactions = db.query(Transaction).all()
    db.close()
    return jsonify([
        {
            "trasaction_id":t.transaction_id,
            "customer_id":t.customer_id,
            "product_id":t.product_id,
            "purchase_date":t.purchase_date
        }for t in transactions
    ])

@router.route('/transactions/<int:transaction_id>',methods = ['GET'])
def get_by_id(transaction_id):
    db=SessionLocal()
    transaction = db.query(Transaction).get(transaction_id)
    db.close()
    if transaction:
        return jsonify({
            "trasaction_id":transaction.transaction_id,
            "customer_id":transaction.customer_id,
            "product_id":transaction.product_id,
            "purchase_date":transaction.purchase_date
        })
    return jsonify({"error": "transaction not found"}), 404

@router.route('/transactions/<int:transaction_id>',methods=['PUT'])
def update(transaction_id):
    db=SessionLocal()
    transaction = db.query(Transaction).get(transaction_id)
    if not transaction:
        db.close()
        return jsonify ({"error":"transaction not found"}),404
    data = request.json
    transaction.customer_id = data.get('customer_id', transaction.customer_id)
    transaction.product_id = data.get('product_id', transaction.product_id)
    transaction.purchase_date = data.get('purchase_date', transaction.purchase_date)

    db.commit()
    db.refresh(transaction)
    db.close()
    return jsonify({
         "trasaction_id":transaction.transaction_id,
            "customer_id":transaction.customer_id,
            "product_id":transaction.product_id,
            "purchase_date":transaction.purchase_date
    })

@router.route('/transactions/<int:transaction_id>', methods=['DELETE'])
def delete_customer(transaction_id):
    db = SessionLocal()
    transaction = db.query(Transaction).get(transaction_id)
    if not transaction:
        db.close()
        return jsonify({"error": "transaction not found"}), 404

    db.delete(transaction)
    db.commit()
    db.close()
    return jsonify({"message": "transaction deleted"})    
