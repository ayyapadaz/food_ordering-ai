from db import get_connection
from datetime import datetime

def create_order(user_id,restaurant_id,total_amount):
      conn=get_connection()
      cursor=conn.cursor()
      created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

      cursor.execute("""INSERT INTO orders (user_id,restaurant_id,total_amount,status,created_at) VALUES (?,?,?,?,?)""",(user_id,restaurant_id,total_amount,"Placed",created_at))
      conn.commit()
      order_id=cursor.lastrowid
      conn.close()
      return order_id

def add_order_item(order_id,food_id,quantity,price):
      conn=get_connection()
      cursor=conn.cursor()
      cursor.execute("""INSERT INTO order_items (order_id,food_id,quantity,price) VALUES (?,?,?,?)""",(order_id,food_id,quantity,price))
      conn.commit()
      conn.close()

def get_orders_with_food():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""SELECT
            orders.id,
            restaurants.name,
            food_items.name,
            order_items.quantity,
            order_items.price,
            orders.total_amount,
            orders.status,
            orders.created_at

        FROM orders

        JOIN restaurants
            ON orders.restaurant_id = restaurants.id

        JOIN order_items
            ON orders.id = order_items.order_id

        JOIN food_items
            ON order_items.food_id = food_items.id
    """)

    rows = cursor.fetchall()

    result = []

    for row in rows:
        result.append({
            "order_id": row[0],
            "restaurant": row[1],
            "food_name": row[2],
            "quantity": row[3],
            "price": row[4],
            "item_total": row[3] * row[4],
            "order_total": row[5],
            "status": row[6],
            "created_at": row[7]
        })

    conn.close()

    return result

def delete_order(order_id):
      conn=get_connection()
      cursor=conn.cursor()

      cursor.execute("""DELETE FROM orders WHERE id=?""",(order_id,))
      conn.commit()
      deleted =cursor.rowcount
      conn.close()
      return deleted

def get_orders_by_user(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""SELECT
            orders.id,
            restaurants.name,
            food_items.name,
            order_items.quantity,
            order_items.price,
            orders.total_amount,
            orders.status,
            orders.created_at

        FROM orders

        JOIN restaurants
            ON orders.restaurant_id = restaurants.id

        JOIN order_items
            ON orders.id = order_items.order_id

        JOIN food_items
            ON order_items.food_id = food_items.id

        WHERE orders.user_id = ? """, (user_id,))

    rows = cursor.fetchall()
    conn.close()

    result = []

    for row in rows:
        result.append({
            "order_id": row[0],
            "restaurant": row[1],
            "food_name": row[2],
            "quantity": row[3],
            "price": row[4],
            "item_total": row[3] * row[4],
            "order_total": row[5],
            "status": row[6],
            "created_at": row[7]
        })
    return result

def get_order_by_id(order_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""SELECT
            orders.id,
            restaurants.name,
            food_items.name,
            order_items.quantity,
            order_items.price,
            orders.total_amount,
            orders.status,
            orders.created_at

        FROM orders

        JOIN restaurants
            ON orders.restaurant_id = restaurants.id

        JOIN order_items
            ON orders.id = order_items.order_id

        JOIN food_items
            ON order_items.food_id = food_items.id

        WHERE orders.id = ?""", (order_id,))

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return None

    items = []

    for row in rows:
        items.append({
            "food_name": row[2],
            "quantity": row[3],
            "price": row[4],
            "item_total": row[3] * row[4]
        })

    return {
        "order_id": rows[0][0],
        "restaurant": rows[0][1],
        "order_total": rows[0][5],
        "status": rows[0][6],
        "created_at": rows[0][7],
        "items": items
    }

def update_order_status(order_id, status):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE orders
        SET status = ?
        WHERE id = ?
    """, (status, order_id))

    conn.commit()
    updated = cursor.rowcount
    conn.close()
    return updated