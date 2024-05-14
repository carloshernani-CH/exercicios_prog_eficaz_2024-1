from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson import ObjectId
from datetime import datetime

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb+srv://admin:admin@projagil.wxdih1t.mongodb.net/desafio'
mongo = PyMongo(app)

def convert_object_id(doc):
    if isinstance(doc, dict):
        for key, value in doc.items():
            if isinstance(value, ObjectId):
                doc[key] = {'$oid': str(value)}
            elif isinstance(value, list):
                doc[key] = [convert_object_id(item) for item in value]
            elif isinstance(value, dict):
                doc[key] = convert_object_id(value)
    elif isinstance(doc, list):
        doc = [convert_object_id(item) for item in doc]
    return doc

def convert_oid_to_objectid(doc):
    if isinstance(doc, dict):
        for key, value in doc.items():
            if isinstance(value, dict) and '$oid' in value:
                doc[key] = ObjectId(value['$oid'])
            elif isinstance(value, list):
                doc[key] = [convert_oid_to_objectid(item) for item in value]
            elif isinstance(value, dict):
                doc[key] = convert_oid_to_objectid(value)
    elif isinstance(doc, list):
        doc = [convert_oid_to_objectid(item) for item in doc]
    return doc

##################################################################################
# CLIENTES

# lista de todos os clientes
@app.route('/clientes', methods=['GET'])
def get_all_clients():
    filtro = {}
    dados_clientes = mongo.db.clientes.find(filtro)
    clientes = []
    for cliente in dados_clientes:
        cliente = convert_object_id(cliente)
        clientes.append(cliente)
    return jsonify(clientes), 200

# postar novo cliente
@app.route('/clientes', methods=['POST'])
def post_client():
    data = request.json
    result = mongo.db.clientes.insert_one(data)
    return {"id": {'$oid': str(result.inserted_id)}, "OK": "Cliente cadastrado com sucesso"}, 201

# cliente por id
@app.route('/clientes/<string:id_cliente>', methods=['GET'])
def client_get_id(id_cliente):
    filtro = {"_id": ObjectId(id_cliente)}
    cliente = mongo.db.clientes.find_one(filtro)
    if cliente:
        cliente = convert_object_id(cliente)
        return jsonify(cliente), 200
    else:
        return {'mensagem': 'cliente não encontrado'}, 404

# atualizar cliente
@app.route('/clientes/<string:id_cliente>', methods=['PUT'])
def update_client(id_cliente):
    data = request.json
    filtro = {"_id": ObjectId(id_cliente)}
    cliente = mongo.db.clientes.find_one(filtro)
    if not cliente:
        return {"erro": "cliente não encontrado"}, 404
    else:
        mongo.db.clientes.update_one(filtro, {"$set": data})
        return {'mensagem': 'Cliente atualizado com sucesso'}, 201

# deletar cliente
@app.route('/clientes/<string:id_cliente>', methods=['DELETE'])
def delete_client(id_cliente):
    filtro = {"_id": ObjectId(id_cliente)}
    client = mongo.db.clientes.find_one(filtro)
    if not client:
        return {"erro": "cliente não encontrado"}, 404
    else:
        mongo.db.clientes.delete_one(filtro)
        return {'mensagem': 'cliente deletado com sucesso'}, 200

##################################################################################
# PRODUTOS

# lista de todos os produtos
@app.route('/produtos', methods=['GET'])
def get_all_products():
    filtro = {}
    dados_produtos = mongo.db.produtos.find(filtro)
    produtos = []
    for produto in dados_produtos:
        produto = convert_object_id(produto)
        produtos.append(produto)
    return jsonify(produtos), 200

# postar novo produto
@app.route('/produtos', methods=['POST'])
def post_product():
    data = request.json
    result = mongo.db.produtos.insert_one(data)
    return {"id": {'$oid': str(result.inserted_id)}, "OK": "produto cadastrado com sucesso"}, 201

# produto por id
@app.route('/produtos/<string:id_produto>', methods=['GET'])
def product_get_id(id_produto):
    filtro = {"_id": ObjectId(id_produto)}
    produto = mongo.db.produtos.find_one(filtro)
    if produto:
        produto = convert_object_id(produto)
        return jsonify(produto), 200
    else:
        return {'mensagem': 'produto não encontrado'}, 404

# atualizar produto
@app.route('/produtos/<string:id_produto>', methods=['PUT'])
def update_product(id_produto):
    data = request.json
    filtro = {"_id": ObjectId(id_produto)}
    produto = mongo.db.produtos.find_one(filtro)
    if not produto:
        return {"erro": "produto não encontrado"}, 404
    else:
        mongo.db.produtos.update_one(filtro, {"$set": data})
        return {'mensagem': 'produto atualizado com sucesso'}, 201

# deletar produto
@app.route('/produtos/<string:id_produto>', methods=['DELETE'])
def delete_product(id_produto):
    filtro = {"_id": ObjectId(id_produto)}
    product = mongo.db.produtos.find_one(filtro)
    if not product:
        return {"erro": "produto não encontrado"}, 404
    else:
        mongo.db.produtos.delete_one(filtro)
        return {'mensagem': 'produto deletado com sucesso'}, 200

##################################################################################
# PEDIDOS

# lista de todos os pedidos
@app.route('/pedidos', methods=['GET'])
def get_all_orders():
    filtro = {}
    dados_pedidos = mongo.db.pedidos.find(filtro)
    pedidos = []
    for pedido in dados_pedidos:
        pedido = convert_object_id(pedido)
        pedidos.append(pedido)
    return jsonify(pedidos), 200

# postar novo pedido
@app.route('/pedidos', methods=['POST'])
def post_order():
    data = request.json
    data = convert_oid_to_objectid(data)  # Convertendo $oid para ObjectId

    cliente_id = data.get('cliente_id')
    if not cliente_id:
        return {'erro': 'cliente_id é necessário'}, 400
    cliente = mongo.db.clientes.find_one({"_id": cliente_id})
    if not cliente:
        return {'erro': 'Cliente não encontrado'}, 404

    data['data_hora'] = datetime.now().isoformat()
    result = mongo.db.pedidos.insert_one(data)

    pedido = {
        'pedido_id': result.inserted_id,
        'data_hora': data['data_hora'],
        'valor_total': data['valor_total'],
        'status': data['status'],
        'itens': data['itens']
    }

    mongo.db.clientes.update_one({"_id": cliente_id}, {"$push": {"pedidos": pedido}})

    return {"id": {'$oid': str(result.inserted_id)}, "OK": "pedido cadastrado com sucesso"}, 201

# pedido por id
@app.route('/pedidos/<string:id_pedido>', methods=['GET'])
def order_get_id(id_pedido):
    filtro = {"_id": ObjectId(id_pedido)}
    pedido = mongo.db.pedidos.find_one(filtro)
    if pedido:
        pedido = convert_object_id(pedido)
        return jsonify(pedido), 200
    else:
        return {'mensagem': 'pedido não encontrado'}, 404

if __name__ == '__main__':
    app.run(debug=True)
