from flask import Flask, jsonify, request
from pymongo import MongoClient
from product import Product
from decouple import config

app = Flask(__name__)

client = MongoClient(config('MONGO_URI'))
db = client.get_default_database()

productModel = Product(db)

@app.route("/products", methods=['GET'])
def get_products():
    productsList = productModel.get_all()
    return jsonify(productsList)

@app.route("/products/<productId>", methods=['GET'])
def get_product_by_id(productId):
    product = productModel.get_by_id(productId)
    if product:
        return jsonify(product)
    return jsonify({"error":"Producto no encontrado"}), 404

@app.route("/products", methods=['POST'])
def add_product():
    newProduct = request.json
    productId = productModel.add(newProduct)
    return jsonify({"id":str(productId)}), 201

if __name__ == '__main__':
    app.run(debug=True)
