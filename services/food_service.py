from db import get_connection

def get_all_foods():
      conn=get_connection()
      cursor=conn.cursor()
      cursor.execute("SELECT * FROM food_items")
      rows=cursor.fetchall()
      foods=[]
      for row in rows:
            foods.append({
                "id":row[0],
                "name":row[1],
                "price":row[2],
                "category":row[3]
            })
      conn.close()
      return foods

def get_food_by_id(food_id):
      conn=get_connection()
      cursor=conn.cursor()

      cursor.execute("""SELECT * FROM food_items WHERE id=?""",(food_id,))
      row=cursor.fetchone()
      conn.close()

      if row:
            return{
                  "id":row[0],
                "name":row[1],
                "price":row[2],
                "category":row[3]
            }
      return None

def add_food(name, price, category):
      conn = get_connection()
      cursor = conn.cursor()

      cursor.execute(
            """
            INSERT INTO food_items (name, price, category)
            VALUES (?, ?, ?)
            """,
            (name, price, category)
      )

      conn.commit()

      food_id = cursor.lastrowid

      conn.close()

      return food_id

def get_foods_by_category(category):
      conn = get_connection()
      cursor = conn.cursor()

      cursor.execute(
            """
            SELECT * FROM food_items WHERE category=?
            """,
            (category,)
      )

      rows = cursor.fetchall()

      foods = []
      for row in rows:
            foods.append({
                  "id": row[0],
                  "name": row[1],
                  "price": row[2],
                  "category": row[3]
            })

      conn.close()

      return foods

def update_food(food_id, name, price, category):
      conn = get_connection()
      cursor = conn.cursor()

      cursor.execute(
            """
            UPDATE food_items
            SET name=?, price=?, category=?
            WHERE id=?
            """,
            (name, price, category, food_id)
      )

      conn.commit()

      updated = cursor.rowcount

      conn.close()

      return updated

def delete_food(food_id):
      conn = get_connection()
      cursor = conn.cursor()

      cursor.execute(
            "DELETE FROM food_items WHERE id=?",
            (food_id,)
      )

      conn.commit()

      deleted = cursor.rowcount

      conn.close()

      return deleted