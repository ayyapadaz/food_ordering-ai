import bcrypt
from db import get_connection

def add_user(name,email, password, role="customer"):
      conn=get_connection()
      cursor=conn.cursor()

      hashed_password=bcrypt.hashpw(
            password.encode(),
            bcrypt.gensalt()
      ).decode()

      cursor.execute("""INSERT INTO users (name,email,password,role) VALUES (?,?,?,?)""",(name,email,hashed_password,role))
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
                    "email":row[2],
                    "role":row[4]
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
                  "email":row[2],
                    "role":row[4]
            }
      return None

def get_user_by_email(email):
      conn=get_connection()
      cursor=conn.cursor()
      cursor.execute("""SELECT * FROM users WHERE email=?""",(email,))
      row=cursor.fetchone()
      conn.close()
      if row:
            return {
                  "id": row[0],
                  "name": row[1],
                  "email": row[2],
                  "password": row[3],
                  "role": row[4]
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

def verify_user(email,password):
      user=get_user_by_email(email)
      print("USER =", user)

      if not user:
            return None
      valid=bcrypt.checkpw(password.encode(),user["password"].encode())
      print("VALID =", valid)
      if valid:
            return user
      return None
