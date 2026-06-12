from db import get_connection

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
