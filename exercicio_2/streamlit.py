import exercicio_2.streamlit as st
import requests
from datetime import datetime

# URL base da API
api_url = "http://localhost:5000"

# Funções auxiliares para chamadas à API com tratamento de erros
def get_all_clients():
    try:
        response = requests.get(f"{api_url}/clientes")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Erro ao obter clientes: {e}")
        return []

def get_all_products():
    try:
        response = requests.get(f"{api_url}/produtos")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Erro ao obter produtos: {e}")
        return []

def get_all_orders():
    try:
        response = requests.get(f"{api_url}/pedidos")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Erro ao obter pedidos: {e}")
        return []

def post_client(data):
    try:
        response = requests.post(f"{api_url}/clientes", json=data)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Erro ao adicionar cliente: {e}")
        return {}

def post_product(data):
    try:
        response = requests.post(f"{api_url}/produtos", json=data)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Erro ao adicionar produto: {e}")
        return {}

def post_order(data):
    try:
        response = requests.post(f"{api_url}/pedidos", json=data)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Erro ao fazer pedido: {e}")
        return {}

def update_client(id_cliente, data):
    try:
        response = requests.put(f"{api_url}/clientes/{id_cliente}", json=data)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Erro ao atualizar cliente: {e}")
        return {}

def update_product(id_produto, data):
    try:
        response = requests.put(f"{api_url}/produtos/{id_produto}", json=data)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Erro ao atualizar produto: {e}")
        return {}

def update_order(id_pedido, data):
    try:
        response = requests.put(f"{api_url}/pedidos/{id_pedido}", json=data)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Erro ao atualizar pedido: {e}")
        return {}

def delete_client(id_cliente):
    try:
        response = requests.delete(f"{api_url}/clientes/{id_cliente}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Erro ao deletar cliente: {e}")
        return {}

def delete_product(id_produto):
    try:
        response = requests.delete(f"{api_url}/produtos/{id_produto}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Erro ao deletar produto: {e}")
        return {}

def delete_order(id_pedido):
    try:
        response = requests.delete(f"{api_url}/pedidos/{id_pedido}")
        response.raise_for_status()
        if response.content:
            return response.json()
        else:
            return {"mensagem": "Pedido deletado com sucesso"}
    except requests.RequestException as e:
        st.error(f"Erro ao deletar pedido: {e}")
        return {}

# Interface Streamlit
st.title("Sistema de Gestão")

# Seleção do Painel
painel = st.sidebar.selectbox("Selecione o Painel", ["Usuário", "Administrativo"])

if painel == "Usuário":
    st.header("Painel do Usuário")

    # Visualização de Produtos
    st.subheader("Produtos")
    produtos = get_all_products()
    for produto in produtos:
        st.write(f"Nome: {produto['nome']}, Descrição: {produto['descricao']}, Preço: {produto['preco']}")

    # Fazer Pedido
    st.subheader("Fazer Pedido")
    cliente_id = st.text_input("ID do Cliente")
    produto_id = st.text_input("ID do Produto")
    quantidade = st.number_input("Quantidade", min_value=1)
    if st.button("Fazer Pedido"):
        pedido = {
            "cliente_id": {"$oid": cliente_id},
            "data_hora": datetime.now().isoformat(),
            "itens": [{"produto_id": {"$oid": produto_id}, "quantidade": quantidade}],
            "status": "em andamento",
            "valor_total": 0  # Valor total precisa ser calculado
        }
        response = post_order(pedido)
        st.write(response)

elif painel == "Administrativo":
    st.header("Painel Administrativo")

    # Gestão de Clientes
    st.subheader("Clientes")
    clientes = get_all_clients()
    for cliente in clientes:
        st.write(f"ID: {cliente['_id']['$oid']}, Nome: {cliente['nome']}, Email: {cliente['email']}, CPF: {cliente['cpf']}")

    # Adicionar Novo Cliente
    st.subheader("Adicionar Novo Cliente")
    nome_cliente = st.text_input("Nome do Cliente")
    email_cliente = st.text_input("Email do Cliente")
    cpf_cliente = st.text_input("CPF do Cliente")
    senha_cliente = st.text_input("Senha do Cliente", type='password')
    if st.button("Adicionar Cliente"):
        novo_cliente = {
            "nome": nome_cliente,
            "email": email_cliente,
            "cpf": cpf_cliente,
            "senha": senha_cliente
        }
        response = post_client(novo_cliente)
        st.write(response)

    # Atualizar Cliente
    st.subheader("Atualizar Cliente")
    id_cliente = st.text_input("ID do Cliente para Atualizar")
    nome_cliente_upd = st.text_input("Novo Nome do Cliente")
    email_cliente_upd = st.text_input("Novo Email do Cliente")
    cpf_cliente_upd = st.text_input("Novo CPF do Cliente")
    senha_cliente_upd = st.text_input("Nova Senha do Cliente", type='password')
    if st.button("Atualizar Cliente"):
        cliente_atualizado = {
            "nome": nome_cliente_upd,
            "email": email_cliente_upd,
            "cpf": cpf_cliente_upd,
            "senha": senha_cliente_upd
        }
        response = update_client(id_cliente, cliente_atualizado)
        st.write(response)

    # Deletar Cliente
    st.subheader("Deletar Cliente")
    id_cliente_del = st.text_input("ID do Cliente para Deletar")
    if st.button("Deletar Cliente"):
        response = delete_client(id_cliente_del)
        st.write(response)

    # Gestão de Produtos
    st.subheader("Produtos")
    produtos = get_all_products()
    for produto in produtos:
        st.write(f"ID: {produto['_id']['$oid']}, Nome: {produto['nome']}, Descrição: {produto['descricao']}, Preço: {produto['preco']}")

    # Adicionar Novo Produto
    st.subheader("Adicionar Novo Produto")
    nome_produto = st.text_input("Nome do Produto")
    descricao_produto = st.text_input("Descrição do Produto")
    preco_produto = st.number_input("Preço do Produto", min_value=0.0, format="%.2f")
    estoque_produto = st.number_input("Estoque do Produto", min_value=0)
    if st.button("Adicionar Produto"):
        novo_produto = {
            "nome": nome_produto,
            "descricao": descricao_produto,
            "preco": preco_produto,
            "estoque": estoque_produto
        }
        response = post_product(novo_produto)
        st.write(response)

    # Atualizar Produto
    st.subheader("Atualizar Produto")
    id_produto = st.text_input("ID do Produto para Atualizar")
    nome_produto_upd = st.text_input("Novo Nome do Produto")
    descricao_produto_upd = st.text_input("Nova Descrição do Produto")
    preco_produto_upd = st.number_input("Novo Preço do Produto", min_value=0.0, format="%.2f")
    estoque_produto_upd = st.number_input("Novo Estoque do Produto", min_value=0)
    if st.button("Atualizar Produto"):
        produto_atualizado = {
            "nome": nome_produto_upd,
            "descricao": descricao_produto_upd,
            "preco": preco_produto_upd,
            "estoque": estoque_produto_upd
        }
        response = update_product(id_produto, produto_atualizado)
        st.write(response)

    # Deletar Produto
    st.subheader("Deletar Produto")
    id_produto_del = st.text_input("ID do Produto para Deletar")
    if st.button("Deletar Produto"):
        response = delete_product(id_produto_del)
        st.write(response)

    # Gestão de Pedidos
    st.subheader("Pedidos")
    pedidos = get_all_orders()
    for pedido in pedidos:
        st.write(f"ID do Pedido: {pedido['_id']['$oid']}, Cliente ID: {pedido['cliente_id']['$oid']}, Data: {pedido['data_hora']}, Status: {pedido['status']}, Valor Total: {pedido['valor_total']}")




