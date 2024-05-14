import streamlit as st
import requests
import json
from datetime import datetime

# URL base da API
api_url = "http://localhost:5000"

# Funções auxiliares para chamadas à API
def get_all_clients():
    response = requests.get(f"{api_url}/clientes")
    return response.json()

def get_all_products():
    response = requests.get(f"{api_url}/produtos")
    return response.json()

def get_all_orders():
    response = requests.get(f"{api_url}/pedidos")
    return response.json()

def post_client(data):
    response = requests.post(f"{api_url}/clientes", json=data)
    return response.json()

def post_product(data):
    response = requests.post(f"{api_url}/produtos", json=data)
    return response.json()

def post_order(data):
    response = requests.post(f"{api_url}/pedidos", json=data)
    return response.json()

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
        st.write(f"Nome: {cliente['nome']}, Email: {cliente['email']}, CPF: {cliente['cpf']}")

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

    # Gestão de Produtos
    st.subheader("Produtos")
    produtos = get_all_products()
    for produto in produtos:
        st.write(f"Nome: {produto['nome']}, Descrição: {produto['descricao']}, Preço: {produto['preco']}")

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

    # Gestão de Pedidos
    st.subheader("Pedidos")
    pedidos = get_all_orders()
    for pedido in pedidos:
        st.write(f"ID do Pedido: {pedido['_id']['$oid']}, Cliente ID: {pedido['cliente_id']['$oid']}, Data: {pedido['data_hora']}, Status: {pedido['status']}, Valor Total: {pedido['valor_total']}")
