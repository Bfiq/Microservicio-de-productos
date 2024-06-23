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

@app.route("/products/<productId>", methods=['PATCH'])
def update_partial_product(productId):
    data = request.json
    updatedCount = productModel.update(productId,data,partial=True)
    if updatedCount > 0:
        return jsonify({"message":"Producto actualizado"}), 200
    return jsonify({"message":"Error al actualizar el producto"}), 404

@app.route("/products/<productId>", methods=['PUT'])
def update_full_product(productId):
    data = request.json
    updatedCount = productModel.update(productId,data,partial=False)
    if updatedCount > 0:
        return jsonify({"message":"Producto actualizado"}), 200
    return jsonify({"message":"Error al actualizar el producto"}), 404

if __name__ == '__main__':
    app.run(debug=True)
