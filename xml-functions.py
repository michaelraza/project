import streamlit as st  # type: ignore
import json
from functools import reduce

# Exemples de données
example_cart = [
    {"id": 1, "userId": 1, "date": "2020-03-02T00:00:00.000Z", "products": [{"productId": 1, "quantity": 4}, {"productId": 2, "quantity": 1}, {"productId": 3, "quantity": 6}], "__v": 0},
    {"id": 2, "userId": 1, "date": "2020-01-02T00:00:00.000Z", "products": [{"productId": 2, "quantity": 4}, {"productId": 1, "quantity": 10}, {"productId": 5, "quantity": 2}], "__v": 0}
]

example_products = [
    {"id": 1, "title": "Backpack", "price": 109.95}, 
    {"id": 2, "title": "T-Shirt", "price": 22.3},
    {"id": 3, "title": "Jacket", "price": 55.99},
    {"id": 5, "title": "Bracelet", "price": 695}
]

# Fonction map
def map_operation(data):
    return [{"userId": cart["userId"], "productIds": [p["productId"] for p in cart["products"]]} for cart in data]

# Fonction filter
def filter_operation(data):
    return [cart for cart in data if len(cart["products"]) > 2]

# Fonction reduce
def reduce_operation(data):
    return reduce(lambda x, y: x + len(y["products"]), data, 0)

# Interface Streamlit
st.title("Transformation de données JSON")

# Input JSON des utilisateurs
cart_input = st.text_area("Entrer les données du panier (cart)", value=json.dumps(example_cart))
products_input = st.text_area("Entrer les données des produits", value=json.dumps(example_products))

# Convertir les données en format JSON
try:
    cart_data = json.loads(cart_input)
    products_data = json.loads(products_input)
except json.JSONDecodeError:
    st.error("Erreur de format JSON")

# Boutons d'opérations
if st.button("Appliquer map"):
    result_map = map_operation(cart_data)
    st.json(result_map)

if st.button("Appliquer filter"):
    result_filter = filter_operation(cart_data)
    st.json(result_filter)

if st.button("Appliquer reduce"):
    result_reduce = reduce_operation(cart_data)
    st.write(f"Total de produits: {result_reduce}")

# Visualisation des données
st.subheader("Données Cart transformées")
st.json(cart_data)
