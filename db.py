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