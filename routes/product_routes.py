from flask import Blueprint, request, jsonify
from database import SessionLocal
from models.product import Product

router = Blueprint('products', __name__)

@router.route('/products',methods=['POST'])
def add_product():
    db=SessionLocal()
    data=request.json
    product = Product(name = data.get('name'),
                        category = data.get('category'),
                        price = data.get('price')
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    db.close()
    return jsonify({"product_id":product.product_id})

@router.route('/products',methods = ['GET'])
def get_all():
    db = SessionLocal()
    products = db.query(Product).all()
    db.close()
    return jsonify([
        {
            "product_id":c.product_id,
            "name":c.name,
            "category":c.category,
            "price":c.price
        }for c in products
    ])

@router.route('/products/<int:product_id>',methods = ['GET'])
def get_by_id(product_id):
    db=SessionLocal()
    product = db.query(Product).get(product_id)
    db.close()
    if product:
        return jsonify({
            "product_id":product.product_id,
            "name":product.name,
            "category":product.category,
            "price":product.price
        })
    return jsonify({"error": "Product not found"}), 404

@router.route('/products/<int:product_id>',methods=['PUT'])
def update(product_id):
    db=SessionLocal()
    product = db.query(Product).get(product_id)
    if not product:
        db.close()
        return jsonify ({"error":"product not found"}),404
    data = request.json
    product.name = data.get('name', product.name)
    product.category = data.get('category', product.category)
    product.price = data.get('price', product.price)

    db.commit()
    db.refresh(product)
    db.close()
    return jsonify({
        "product_id":product.product_id,
        "name":product.name,
        "category":product.category,
        "price":product.price
    })

@router.route('/products/<int:product_id>', methods=['DELETE'])
def delete(product_id):
    db = SessionLocal()
    product = db.query(Product).get(product_id)
    if not product:
        db.close()
        return jsonify({"error": "product not found"}), 404

    db.delete(product)
    db.commit()
    db.close()
    return jsonify({"message": "Product deleted"})    
