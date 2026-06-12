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
    restaurant_id INTEGER NOT NULL,
    total_amount REAL NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL,

    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(restaurant_id) REFERENCES restaurants(id))""")
     
     cursor.execute("""CREATE TABLE IF NOT EXISTS order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    food_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL,

    FOREIGN KEY(order_id) REFERENCES orders(id),
    FOREIGN KEY(food_id) REFERENCES food_items(id))""")
     

     cursor.execute("""CREATE TABLE IF NOT EXISTS restaurants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    cuisine TEXT NOT NULL,
    rating REAL NOT NULL)""")
     cursor.execute("""CREATE TABLE IF NOT EXISTS restaurant_menu (
     id INTEGER PRIMARY KEY AUTOINCREMENT,
     restaurant_id INTEGER NOT NULL,
     food_id INTEGER NOT NULL,
     price REAL NOT NULL,
     FOREIGN KEY(restaurant_id) REFERENCES restaurants(id),
     FOREIGN KEY(food_id) REFERENCES food_items(id))""")
     cursor.execute("""CREATE TABLE IF NOT EXISTS cart (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    restaurant_id INTEGER NOT NULL,

    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(restaurant_id) REFERENCES restaurants(id))""")
     cursor.execute("""CREATE TABLE IF NOT EXISTS cart_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cart_id INTEGER NOT NULL,
    menu_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,

    FOREIGN KEY(cart_id) REFERENCES cart(id),
    FOREIGN KEY(menu_id) REFERENCES restaurant_menu(id))""")

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













