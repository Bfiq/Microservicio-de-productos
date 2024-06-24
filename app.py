from flask import Flask, jsonify, request
from pymongo import MongoClient
from product import Product
from decouple import config
import uuid
from azure.storage.blob import BlobClient

app = Flask(__name__)

client = MongoClient(config('MONGO_URI'))
db = client.get_default_database()

productModel = Product(db)

#blob container
sas_url_container = config('URL_SAS_AZURE_BLOB_CONTAINER')
container_url = sas_url_container.split('?')[0]  # URL base del contenedor
sas_token = sas_url_container.split('?')[1]      # Token SAS

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
    if 'file' not in request.files:
        return jsonify({"message":"No hay una imagen agregada"}), 400

    if len(request.files)>1:
        return jsonify({"message":"hay mas de una imagen"}), 400
    
    file = request.files['file']
    
    if file.filename =='':
        return jsonify({"message":"ha habido un error con la imagen"})
    
    filename = str(uuid.uuid4())+"-"+file.filename

    try:
        #creación del cliente
        blob_client = BlobClient.from_blob_url(container_url + '/' + filename + '?' + sas_token)
        
        # Subir el archivo
        blob_client.upload_blob(file)
        
        # URL del archivo subido
        file_url = container_url + '/' + filename

        newProduct = request.form.to_dict()
        newProduct['productImage']= file_url

        productId = productModel.add(newProduct)
        return jsonify({"id":str(productId)}), 201
    except Exception as e:
        return jsonify({"message":"Error al subir la imagen"}), 500


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
