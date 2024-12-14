from flask import Flask, request, jsonify
import pymysql
app = Flask(__name__)
# Database connection details
db_connection = pymysql.connect(
 host="<RDS-ENDPOINT>", # Replace with your RDS endpoint
 user="admin", # Replace with your RDS master username
 password="MyStrongPassword123", # Replace with your RDS master password
 database="EcommerceDB"
)
# Route to insert data into the database
@app.route('/add-product', methods=['POST'])
def add_product():
 data = request.json
 name = data['name']
 price = data['price']
 stock = data['stock']
try:
 with db_connection.cursor() as cursor:
 query = "INSERT INTO Products (Name, Price, Stock) VALUES (%s, %s, %s)"
 cursor.execute(query, (name, price, stock))
 db_connection.commit()
 return jsonify({"message": "Product added successfully!"}), 201
 except Exception as e:
 return jsonify({"error": str(e)}), 500
# Route to retrieve products
@app.route('/products', methods=['GET'])
def get_products():
 try:
 with db_connection.cursor() as cursor:
 cursor.execute("SELECT * FROM Products")
 results = cursor.fetchall()
 products = [{"id": row[0], "name": row[1], "price": row[2], "stock": row[3]} for row in results]
 return jsonify(products), 200
 except Exception as e:
 return jsonify({"error": str(e)}), 500
if __name__ == '__main__':
 app.run(host='0.0.0.0', port=5000)
