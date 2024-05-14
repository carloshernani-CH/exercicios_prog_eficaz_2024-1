#postar novo pedido
@app.route('/pedidos', methods = ['POST'])
def post_order():
    data = request.json
    
    result = mongo.db.pedidos.insert_one(data)

    return {"id": str(result.inserted_id), "OK":"pedido cadastrado com sucesso"}, 201

#pedido por id
@app.route('/pedidos/<string:id_pedido>', methods=['GET'])
def order_get_id(id_pedido):
    filtro = {"_id": ObjectId(id_pedido)}

    pedido = mongo.db.pedidos.find_one(filtro)
    if pedido:
        return {'pedido': str(pedido)}
    else:
        return {'mensagem':'pedido não encontrado'}, 404