from db import get_connection

def get_total_orders():
      conn=get_connection()
      cursor=conn.cursor()
      cursor.execute("""SELECT COUNT(*) FROM ORDERS""")
      total=cursor.fetchone()[0]
      conn.close()
      return total

def get_total_revenue():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT SUM(total_amount)
        FROM orders""")

    revenue = cursor.fetchone()[0]
    conn.close()
    return revenue or 0

def get_top_food():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            food_items.name,
            SUM(order_items.quantity) AS total_quantity
        FROM order_items
        JOIN food_items
            ON order_items.food_id = food_items.id
        GROUP BY food_items.name
        ORDER BY total_quantity DESC
        LIMIT 1
    """)

    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "food_name": row[0],
            "total_quantity": row[1]
        }

    return None

def get_top_customer():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            users.name,
            SUM(order_items.price * order_items.quantity) AS total_spent

        FROM orders

        JOIN users
            ON orders.user_id = users.id

        JOIN order_items
            ON orders.id = order_items.order_id

        GROUP BY users.id

        ORDER BY total_spent DESC

        LIMIT 1
    """)

    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "customer_name": row[0],
            "total_spent": row[1]
        }

    return None
