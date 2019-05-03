from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#init db
db = SQLAlchemy(app)
# init ma
ma = Marshmallow(app)

# Product Class/Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    image_file = db.Column(db.Text)

    def __init__(self, name, image_file):
        self.name = name
        self.image_file = image_file

# Product Schema
class ProductSchema(ma.Schema):
    class Meta:
        fields  = ('name','image_file')

# Init schema
product_schema = ProductSchema(strict=True)
products_schema = ProductSchema(many=True, strict=True)

# Create a Product
@app.route('/')
@app.route('/product', methods=['POST'])
def add_product():
    name = request.json['name']
    image_file = request.json['image_file']
 
    new_product = Product(name, image_file)

    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)

# Get All Products
@app.route('/product', methods=['GET'])
def get_prducts():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result.data)

# Get Single Products
@app.route('/product/<id>', methods=['GET'])
def get_prduct(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)

# Update a Product
@app.route('/product/<id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)

    name = request.json['name']
    image_file = request.json['image_file']

    product.name = name
    product.image_file = image_file

    db.session.commit()

    return product_schema.jsonify(product)

# Delete Product
@app.route('/product/<id>', methods=['DELETE'])
def delete_prduct(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()

    return product_schema.jsonify(product)


# Run server
if __name__ == '__main__':
	app.run(debug=True)
