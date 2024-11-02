from flask import Flask, request, jsonify
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

# Contoh data produk bodycare
bodycare_products = [
    {
        "id": 1,
        "name": "Body Lotion Lavender",
        "description": "Body lotion dengan aroma lavender yang menenangkan.",
        "price": 100,  # dalam ribuan
        "address": "Jl. Lavender No.10, Jakarta"
    },
    {
        "id": 2,
        "name": "Body Scrub Kopi",
        "description": "Body scrub dengan ekstrak kopi untuk mengangkat sel kulit mati.",
        "price": 120,  # dalam ribuan
        "address": "Jl. Kopi No.20, Bandung"
    },
    {
        "id": 3,
        "name": "Body Wash Green Tea",
        "description": "Sabun mandi dengan kandungan green tea untuk melembutkan kulit.",
        "price": 90,  # dalam ribuan
        "address": "Jl. Green Tea No.15, Yogyakarta"
    }
]

class BodycareProductList(Resource):
    def get(self):
        return jsonify(bodycare_products)

class BodycareProductDetail(Resource):
    def get(self, product_id):
        product = next((p for p in bodycare_products if p["id"] == product_id), None)
        if product:
            return jsonify(product)
        return {"message": "Product not found"}, 404

class AddBodycareProduct(Resource):
    def post(self):
        data = request.get_json()
        new_product = {
            "id": len(bodycare_products) + 1,
            "name": data["name"],
            "description": data.get("description", "No description provided"),
            "price": data["price"],
            "address": data.get("address", "No address provided")
        }
        bodycare_products.append(new_product)
        return jsonify(new_product)

class UpdateBodycareProduct(Resource):
    def put(self, product_id):
        product = next((p for p in bodycare_products if p["id"] == product_id), None)
        if not product:
            return {"message": "Product not found"}, 404
        data = request.get_json()
        product.update(data)
        return jsonify(product)

class DeleteBodycareProduct(Resource):
    def delete(self, product_id):
        global bodycare_products
        bodycare_products = [p for p in bodycare_products if p["id"] != product_id]
        return {"message": "Product deleted successfully"}

# Menambahkan resource ke API
api.add_resource(BodycareProductList, '/bodycare-products')
api.add_resource(BodycareProductDetail, '/bodycare-products/<int:product_id>')
api.add_resource(AddBodycareProduct, '/bodycare-products/add')
api.add_resource(UpdateBodycareProduct, '/bodycare-products/update/<int:product_id>')
api.add_resource(DeleteBodycareProduct, '/bodycare-products/delete/<int:product_id>')

if __name__ == '__main__':
    app.run(debug=True)
