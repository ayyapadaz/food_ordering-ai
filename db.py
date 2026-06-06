import sqlite3
def get_connection():
     return sqlite3.connect("database.db")
    
def init_db():
     conn=get_connection()
     cursor=conn.cursor()
     cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL,
                   email TEXT UNIQUE NOT NULL)""")
    
     cursor.execute("""CREATE TABLE IF NOT EXISTS food_items (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL,
                   price REAL NOT NULL,
                   category TEXT NOT NULL)""")
    
     cursor.execute("""CREATE TABLE IF NOT EXISTS orders (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   user_id INTEGER NOT NULL,
                   food_id INTEGER NOT NULL,
                   quantity INTEGER NOT NULL,
                   
                   FOREIGN KEY(user_id) REFERENCES users(id),
                   FOREIGN KEY(food_id) REFERENCES food_items(id))""")
     
     conn.commit()
     conn.close()


def seed_food():
     conn=get_connection()
     cursor=conn.cursor()
     cursor.execute("SELECT COUNT(*) FROM food_items")
     count = cursor.fetchone()[0]
     if count==0:
            food_items=[
                ("Pizza",250,"Main Course"),
                ("Burger",150,"Main Course"),
                ("Fries",100,"Sides"),
                ("Coke",50,"Beverages"),
                ("Pasta",220,"Main Course"),
                ("Garlic Bread",120,"Sides"),
                ("Chicken Wings",180,"Starters"),
                ("Ice Cream",90,"Dessert")
            ]
            cursor.executemany("INSERT INTO food_items (name,price,category) VALUES (?,?,?)",food_items)
            conn.commit()
     conn.close()

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


def add_orders(user_id,food_id,quantity):
      conn=get_connection()
      cursor=conn.cursor()

      cursor.execute("""INSERT INTO orders (user_id, food_id, quantity) VALUES (?,?,?)""",(user_id, food_id, quantity))
      conn.commit()

      order_id=cursor.lastrowid
      conn.close()
      return order_id

def get_order_db():
      conn=get_connection()
      cursor=conn.cursor()
      cursor.execute("""SELECT * FROM orders""")
      rows=cursor.fetchall()
      conn.close()
      orders=[]

      for row in rows:
            orders.append({
                  "id":row[0],
                  "user_id":row[1],
                  "food_id":row[2],
                  "quantity":row[3]
            }) 
      return orders          

def get_orders_with_food():
      conn=get_connection()
      cursor=conn.cursor()
      
      cursor.execute("""SELECT orders.id,food_items.name,food_items.price,orders.quantity
                        FROM orders
                        JOIN food_items ON orders.food_id = food_items.id""")
      rows=cursor.fetchall()

      result=[]

      for row in rows:
            result.append({
                  "order_id":row[0],
                  "food_name":row[1],
                  "price":row[2],
                  "quantity":row[3],
                  "total_price":row[2]*row[3]
            })
      conn.close()
      return result

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

def delete_order(order_id):
      conn=get_connection()
      cursor=conn.cursor()

      cursor.execute("""DELETE FROM orders WHERE id=?""",(order_id,))
      conn.commit()
      deleted =cursor.rowcount
      conn.close()
      return deleted

def update_order(order_id,quantity):
      conn=get_connection()
      cursor=conn.cursor()

      cursor.execute("""UPDATE orders SET quantity=? WHERE id=?""",(quantity,order_id))
      conn.commit()
      updated =cursor.rowcount
      conn.close()
      return updated

def add_user(name,email):
      conn=get_connection()
      cursor=conn.cursor()

      cursor.execute("""INSERT INTO users (name,email) VALUES (?,?)""",(name,email))
      conn.commit()

      user_id=cursor.lastrowid
      conn.close()
      return user_id

def get_user():
      conn=get_connection()
      cursor=conn.cursor()
      cursor.execute("""SELECT * FROM users""")
      rows=cursor.fetchall()
      users=[]
      for row in rows:
            users.append({
                    "id":row[0],
                    "name":row[1],
                    "email":row[2]
            }) 
      conn.close()
      return users

def get_user_by_id(user_id):
      conn=get_connection()
      cursor=conn.cursor()
      cursor.execute("""SELECT * FROM users WHERE id=?""",(user_id,))

      row=cursor.fetchone()
      conn.close()
      if row:
            return {
                  "id":row[0],
                  "name":row[1],
                  "email":row[2]
            }
      return None

def update_user(user_id,name,email):
      conn=get_connection()
      cursor=conn.cursor()

      cursor.execute("""UPDATE users SET name=?, email=? WHERE id=?""",(name,email,user_id))
      conn.commit()
      updated=cursor.rowcount
      conn.close()
      return updated

def delete_user(user_id):
      conn=get_connection()
      cursor=conn.cursor()
      cursor.execute("""DELETE FROM users WHERE id=?""",(user_id,))
      conn.commit()
      deleted=cursor.rowcount
      conn.close()
      return deleted

def get_order_by_id(order_id):
      conn=get_connection()
      cursor=conn.cursor()
      cursor.execute("""SELECT orders.id, food_items.name,food_items.price, orders.quantity
                        FROM orders
                        JOIN food_items ON orders.food_id = food_items.id
                        WHERE orders.id=?""",(order_id,))
      row=cursor.fetchone()
      conn.close()

      if row:
            return {
                  "order_id":row[0],
                  "food_name":row[1],
                  "price":row[2],
                  "quantity":row[3],
                  "total_price":row[2]*row[3]
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

def get_orders_by_user(user_id):
      conn=get_connection()
      cursor=conn.cursor()
      cursor.execute("""SELECT orders.id, food_items.name, food_items.price, orders.quantity
                        FROM orders
                        JOIN food_items ON orders.food_id = food_items.id
                        WHERE orders.user_id=?""",(user_id,))
      rows=cursor.fetchall()
      conn.close()
      result=[]
      for row in rows:
            result.append({
                  "order_id":row[0],
                  "food_name":row[1],
                  "price":row[2],
                  "quantity":row[3],
                  "total_price":row[2]*row[3]
            })
      return result