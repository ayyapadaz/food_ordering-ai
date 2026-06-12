from db import get_connection
from services.order_service import create_order, add_order_item


def get_cart_by_user(user_id):
      conn=get_connection()
      cursor=conn.cursor()

      cursor.execute("""SELECT * FROM cart WHERE user_id=?""", (user_id,))
      row=cursor.fetchone()
      conn.close()
      if row:
            return {
                  "id":row[0],
                  "user_id":row[1],
                  "restaurant_id":row[2]
            }
      return None
def create_cart(user_id, restaurant_id):
      conn = get_connection()
      cursor = conn.cursor()

      cursor.execute(
            """
            INSERT INTO cart (user_id, restaurant_id)
            VALUES (?, ?)
            """,
            (user_id, restaurant_id)
      )

      conn.commit()

      cart_id = cursor.lastrowid

      conn.close()

      return cart_id

def add_cart_item(cart_id, menu_id, quantity):
      conn = get_connection()
      cursor = conn.cursor()

      cursor.execute("""
            INSERT INTO cart_items
            (cart_id, menu_id, quantity)
            VALUES (?, ?, ?)
      """, (cart_id, menu_id, quantity))

      conn.commit()

      item_id = cursor.lastrowid

      conn.close()

      return item_id

def get_cart_details(user_id):
      conn=get_connection()
      cursor=conn.cursor()
      cursor.execute("""SELECT restaurants.name,cart_items.id,food_items.name,restaurant_menu.price,cart_items.quantity
                     FROM cart
                     JOIN restaurants ON cart.restaurant_id=restaurants.id
                     JOIN cart_items ON cart.id = cart_items.cart_id
                     JOIN restaurant_menu ON cart_items.menu_id=restaurant_menu.id
                     JOIN food_items ON restaurant_menu.food_id=food_items.id
                     WHERE cart.user_id=?""",(user_id,))
      rows=cursor.fetchall()
      conn.close()
      return rows

def delete_cart_items(cart_item_id):
      conn=get_connection()
      cursor=conn.cursor()
      cursor.execute("""DELETE FROM cart_items WHERE id=?""",(cart_item_id,))
      conn.commit()
      deleted=cursor.rowcount
      conn.close()
      return deleted

def update_cart_item(cart_item_id,quantity):
      conn=get_connection()
      cursor=conn.cursor()
      cursor.execute("""UPDATE cart_items
                     SET quantity=?
                     WHERE id=?""",(quantity,cart_item_id))
      conn.commit()
      updated=cursor.rowcount
      conn.close()
      return updated

def get_cart_items(cart_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""SELECT
            cart_items.id,
            restaurant_menu.food_id,
            food_items.name,
            restaurant_menu.price,
            cart_items.quantity
        FROM cart_items
        JOIN restaurant_menu
            ON cart_items.menu_id = restaurant_menu.id
        JOIN food_items
            ON restaurant_menu.food_id = food_items.id
        WHERE cart_items.cart_id=?""", (cart_id,))

    rows = cursor.fetchall()
    conn.close()
    items = []
    for row in rows:
        items.append({
            "cart_item_id": row[0],
            "food_id": row[1],
            "food_name": row[2],
            "price": row[3],
            "quantity": row[4]
        })
    return items

def clear_cart_items(cart_id):
      conn = get_connection()
      cursor = conn.cursor()
      cursor.execute("""
        DELETE FROM cart_items
        WHERE cart_id=?""", (cart_id,))
      conn.commit()
      conn.close()

def clear_cart(cart_id):
      conn = get_connection()
      cursor = conn.cursor()
      cursor.execute("""
        DELETE FROM cart
        WHERE id=?""", (cart_id,))
      conn.commit()
      conn.close()

def checkout_cart(user_id):
    cart = get_cart_by_user(user_id)
    if not cart:
        return None

    items = get_cart_items(cart["id"])

    if len(items) == 0:
        return None

    total_amount = 0

    for item in items:
        total_amount += item["price"] * item["quantity"]

    order_id = create_order(user_id,cart["restaurant_id"],total_amount)

    for item in items:
        add_order_item(order_id,item["food_id"],item["quantity"],item["price"])

    clear_cart_items(cart["id"])
    clear_cart(cart["id"])

    return {"order_id": order_id,"total_amount": total_amount}

