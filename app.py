from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS
from bson.objectid import ObjectId

app = Flask(__name__)
CORS(app)

client = MongoClient("mongodb://localhost:27017/")
db = client["cosmeticos_db"]

productos = db["productos"]

# ================= PRODUCTOS =================

@app.route('/productos', methods=['GET'])
def obtener_productos():
    lista = []
    total = 0
    for p in productos.find():
        lista.append({
            "id": str(p["_id"]),
            "nombre": p["nombre"],
            "marca": p["marca"],
            "precio": p["precio"]
        })
        total += p["precio"]
    return jsonify({"productos": lista, "total": total})

@app.route('/productos', methods=['POST'])
def crear_producto():
    data = request.json
    print("DATOS RECIBIDOS:", data)  # 👈 AGREGA ESTO
    productos.insert_one(data)
    return jsonify({"mensaje": "Producto agregado"})

@app.route('/productos/<id>', methods=['PUT'])
def editar_producto(id):
    productos.update_one(
        {"_id": ObjectId(id)},
        {"$set": request.json}
    )
    return jsonify({"mensaje": "Producto actualizado"})

@app.route('/productos/<id>', methods=['DELETE'])
def eliminar_producto(id):
    productos.delete_one({"_id": ObjectId(id)})
    return jsonify({"mensaje": "Producto eliminado"})

if __name__ == '__main__':
    app.run(debug=True)

