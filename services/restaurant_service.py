from db import get_connection

def add_restaurants(name,cuisine,rating):
      conn=get_connection()
      cursor=conn.cursor()

      cursor.execute("""INSERT INTO restaurants (name,cuisine,rating) VALUES (?,?,?)""",(name,cuisine,rating))
      conn.commit()
      restaurant_id=cursor.lastrowid
      conn.close()
      return restaurant_id

def get_restaurants():
      conn=get_connection()
      cursor=conn.cursor()

      cursor.execute("""SELECT * FROM restaurants""")
      rows=cursor.fetchall()
      restaurants=[]
      for row in rows:
            restaurants.append({
                  "id":row[0],
                  "name":row[1],
                  "cuisine":row[2],
                  "rating":row[3]
            })
      conn.close()
      return restaurants

def get_restaurants_by_id(restaurant_id):
      conn=get_connection()
      cursor=conn.cursor()

      cursor.execute("""SELECT * FROM restaurants WHERE id=?""", (restaurant_id,))
      row = cursor.fetchone()
      conn.close()
      if row:
            return {
                  "id": row[0],
                  "name": row[1],
                  "cuisine": row[2],
                  "rating": row[3]
            }
      return None

def update_restaurant(restaurant_id, name, cuisine, rating):
      conn = get_connection()
      cursor = conn.cursor()

      cursor.execute(
            """
            UPDATE restaurants
            SET name=?, cuisine=?, rating=?
            WHERE id=?
            """,
            (name, cuisine, rating, restaurant_id)
      )

      conn.commit()

      updated = cursor.rowcount

      conn.close()

      return updated

def delete_restaurant(restaurant_id):
      conn = get_connection()
      cursor = conn.cursor()

      cursor.execute(
            "DELETE FROM restaurants WHERE id=?",
            (restaurant_id,)
      )

      conn.commit()

      deleted = cursor.rowcount

      conn.close()

      return deleted


def add_menu_item(restaurant_id, food_id, price):
      conn=get_connection()
      cursor=conn.cursor()

      cursor.execute("""INSERT INTO restaurant_menu (restaurant_id, food_id, price)
                     VALUES (?,?,?)""",(restaurant_id, food_id, price))
      conn.commit()
      menu_id=cursor.lastrowid
      conn.close()
      return menu_id

def get_restaurant_menu():
      conn=get_connection()
      cursor=conn.cursor()

      cursor.execute("""SELECT restaurant_menu.id, restaurants.name, food_items.name, restaurant_menu.price
                     FROM restaurant_menu
                     JOIN restaurants ON restaurant_menu.restaurant_id = restaurants.id
                     JOIN food_items ON restaurant_menu.food_id = food_items.id""")
      rows=cursor.fetchall()
      conn.close()
      menu=[]
      for row in rows:
            menu.append({
                  "menu_id":row[0],
                  "restaurant_name":row[1],
                  "food_name":row[2],
                  "price":row[3]
            })
      return menu
def get_menu_by_restaurant(restaurant_id):
      conn=get_connection()
      cursor=conn.cursor()

      cursor.execute("""SELECT food_items.name, restaurant_menu.price
                     FROM restaurant_menu
                     JOIN food_items ON restaurant_menu.food_id = food_items.id
                     WHERE restaurant_menu.restaurant_id=?""",(restaurant_id,))
      rows=cursor.fetchall()
      
      result=[]
      for row in rows:
            result.append({
                  "food_name":row[0],
                  "price":row[1]
            })
      conn.close()
      return result

def get_menu_item_by_id(menu_id):
      conn = get_connection()
      cursor = conn.cursor()

      cursor.execute("""
            SELECT restaurant_id, food_id, price
            FROM restaurant_menu
            WHERE id=?
      """, (menu_id,))

      row = cursor.fetchone()

      conn.close()

      if row:
            return {
                  "restaurant_id": row[0],
                  "food_id": row[1],
                  "price": row[2]
            }

      return None