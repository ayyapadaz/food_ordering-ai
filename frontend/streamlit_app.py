import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:5000"

st.set_page_config(
    page_title="Food Ordering System",
    page_icon="🍔",
    layout="wide"
)

st.title("🍔 Food Ordering System")

# ==========================
# CREATE USER
# ==========================

st.header("Create User")

name = st.text_input("Name")
email = st.text_input("Email")

if st.button("Create User"):
    response = requests.post(
        f"{BASE_URL}/users",
        json={
            "name": name,
            "email": email
        }
    )

    st.success(response.json())

st.divider()

# ==========================
# USERS
# ==========================

st.header("Users")

try:
    users = requests.get(f"{BASE_URL}/users").json()
    st.table(users)

except:
    st.error("Could not load users")

st.divider()

# ==========================
# FOODS
# ==========================

st.header("Foods")

try:
    foods = requests.get(f"{BASE_URL}/foods").json()
    st.table(foods)

except:
    st.error("Could not load foods")

st.divider()

# ==========================
# RESTAURANTS
# ==========================

st.header("Restaurants")

try:
    restaurants = requests.get(f"{BASE_URL}/restaurants").json()
    st.table(restaurants)

except:
    st.error("Could not load restaurants")

st.divider()

# ==========================
# RESTAURANT MENU
# ==========================

st.header("Restaurant Menu")

restaurant_id = st.number_input(
    "Restaurant ID",
    min_value=1,
    step=1,
    key="menu_restaurant"
)

if st.button("Load Menu"):

    try:
        response = requests.get(
            f"{BASE_URL}/restaurants/{restaurant_id}/menu"
        )

        st.table(response.json())

    except:
        st.error("Could not load menu")

st.divider()

# ==========================
# ADD TO CART
# ==========================

st.header("Add Item To Cart")

user_id = st.number_input(
    "User ID",
    min_value=1,
    step=1
)

menu_id = st.number_input(
    "Menu ID",
    min_value=1,
    step=1
)

quantity = st.number_input(
    "Quantity",
    min_value=1,
    step=1
)

if st.button("Add To Cart"):

    response = requests.post(
        f"{BASE_URL}/cart/add",
        json={
            "user_id": int(user_id),
            "menu_id": int(menu_id),
            "quantity": int(quantity)
        }
    )

    st.success(response.json())

st.divider()

# ==========================
# VIEW CART
# ==========================

st.header("View Cart")

cart_user_id = st.number_input(
    "Cart User ID",
    min_value=1,
    step=1,
    key="cart_user"
)

if st.button("Load Cart"):

    try:
        response = requests.get(
            f"{BASE_URL}/cart/{cart_user_id}"
        )

        st.table(response.json())

    except:
        st.error("Could not load cart")

st.divider()

# ==========================
# CHECKOUT
# ==========================

st.header("Checkout")

checkout_user_id = st.number_input(
    "Checkout User ID",
    min_value=1,
    step=1,
    key="checkout_user"
)

if st.button("Checkout"):

    response = requests.post(
        f"{BASE_URL}/checkout/{checkout_user_id}"
    )

    st.success(response.json())

st.divider()

# ==========================
# ORDERS
# ==========================

st.header("Orders")

if st.button("Load Orders"):

    try:
        response = requests.get(
            f"{BASE_URL}/orders"
        )

        orders = response.json()

        st.table(orders)

    except:
        st.error("Could not load orders")

st.divider()

# ==========================
# ORDER STATUS
# ==========================

st.header("Update Order Status")

order_id = st.number_input(
    "Order ID",
    min_value=1,
    step=1,
    key="status_order"
)

status = st.selectbox(
    "Status",
    [
        "Placed",
        "Preparing",
        "Out for Delivery",
        "Delivered",
        "Cancelled"
    ]
)

if st.button("Update Status"):

    try:
        response = requests.put(
            f"{BASE_URL}/orders/{order_id}/status",
            json={
                "status": status
            }
        )

        st.success(response.json())

    except:
        st.error("Could not update status")

st.divider()

# ==========================
# ANALYTICS
# ==========================

st.header("Analytics Dashboard")

col1, col2 = st.columns(2)

try:

    total_orders = requests.get(
        f"{BASE_URL}/analytics/orders"
    ).json()

    revenue = requests.get(
        f"{BASE_URL}/analytics/revenue"
    ).json()

    with col1:
        st.metric(
            "Total Orders",
            total_orders.get("total_orders", 0)
        )

    with col2:
        st.metric(
            "Revenue",
            revenue.get("total_revenue", 0)
        )

except:
    st.warning("Analytics endpoints not available")

try:

    top_food = requests.get(
        f"{BASE_URL}/analytics/top-food"
    ).json()

    st.subheader("Top Food")

    st.write(top_food)

except:
    pass

try:

    top_customer = requests.get(
        f"{BASE_URL}/analytics/top-customer"
    ).json()

    st.subheader("Top Customer")

    st.write(top_customer)

except:
    pass