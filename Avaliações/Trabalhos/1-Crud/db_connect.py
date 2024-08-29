import psycopg2
import bcrypt
from env_vars import DB_HOST, DB_USER, DB_PASSWORD, DB_PORT, DB_NAME

def connect():
    return psycopg2.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)

def createUser(username, password, name):
    try:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        conn = connect()
        cur = conn.cursor()
        
        cur.execute(
            "INSERT INTO \"user\" (username, password, name) VALUES (%s, %s, %s)",
            (username, hashed_password, name)
        )
        
        conn.commit()
        return True
    
    except psycopg2.DatabaseError as error:
        if conn:
            conn.rollback() 
        return None

    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

def getUsers():
    conn = connect()  
    cur = conn.cursor()
    
    cur.execute("SELECT \"id\", \"username\", \"password\", \"name\" FROM \"user\";")
    users = []
    for user in cur.fetchall():
        users.append({
            'id': user[0], 
            'username': user[1], 
            'password': user[2], 
            'name': user[3]
        })
    
    cur.close()
    conn.close()

    return users

def getUserById(id):
    conn = connect()  
    cur = conn.cursor()
    
    cur.execute("SELECT \"id\", \"username\", \"password\", \"name\" FROM \"user\" WHERE \"id\" = %s;", (id,))
    user = cur.fetchone()
    if user:
        user = {'id': user[0], 'username': user[1], 'password': user[2], 'name': user[3]}
    
    cur.close()
    conn.close()

    return user

def getUserByUsername(username):
    conn = connect()  
    cur = conn.cursor()
    
    cur.execute("SELECT \"id\", \"username\", \"password\", \"name\" FROM \"user\" WHERE \"username\" = %s;", (username,))
    user = cur.fetchone()
    if user:
        user = {'id': user[0], 'username': user[1], 'password': user[2], 'name': user[3]}
    
    cur.close()
    conn.close()

    return user


def createWork(courseId, authorId, title, description, price):
    try:
        conn = connect()
        cur = conn.cursor()
        
        cur.execute(
            """
            INSERT INTO \"work\" (course, author, title, description, price) 
            VALUES (%s, %s, %s, %s, %s);
            """,
            (courseId, authorId, title, description, price)
        )
        
        conn.commit()
        return True
    
    except psycopg2.DatabaseError as error:
        print(error)
        if conn:
            conn.rollback() 
        return None

    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

def getWorks():
    conn = connect()
    cur = conn.cursor()
    
    try:
        query = """
            SELECT 
                w.id,
                c.title AS course,
                u.username AS author,
                w.title,
                w.description,
                w.price
            FROM "work" w
            JOIN "course" c ON w.course = c.id
            JOIN "user" u ON w.author = u.id;
        """

        cur.execute(query)
        works = []
        for work in cur.fetchall():
            works.append({
                'id': work[0],
                'course': work[1],
                'author': work[2],
                'title': work[3],
                'description': work[4],
                'price': work[5]
            })
        
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        cur.close()
        conn.close()
    
    return works

def getWorksByUserId(user_id):
    conn = connect()
    cur = conn.cursor()
    
    try:
        query = """
            SELECT 
                w.id,
                c.title AS course,
                u.username AS author,
                w.title,
                w.description,
                w.price
            FROM "work" w
            JOIN "course" c ON w.course = c.id
            JOIN "user" u ON w.author = u.id
            WHERE w.author = %s;
        """
        
        cur.execute(query, (user_id,))
        works = []
        for work in cur.fetchall():
            works.append({
                'id': work[0],
                'course': work[1],
                'author': work[2],
                'title': work[3],
                'description': work[4],
                'price': work[5]
            })
        
    except Exception as e:
        print(f"An error occurred: {e}")
        works = []  # Retorna uma lista vazia em caso de erro
    
    finally:
        cur.close()
        conn.close()
    
    return works

def getWorkById(work_id):
    conn = connect()
    cur = conn.cursor()
    
    try:
        query = """
            SELECT 
                w.id,
                c.title AS course,
                u.username AS author,
                w.title,
                w.description,
                w.price
            FROM "work" w
            JOIN "course" c ON w.course = c.id
            JOIN "user" u ON w.author = u.id
            WHERE w.id = %s;
        """

        cur.execute(query, (work_id,))
        work = cur.fetchone()
        
        if work:
            work_data = {
                'id': work[0],
                'course': work[1],
                'author': work[2],
                'title': work[3],
                'description': work[4],
                'price': work[5]
            }
        else:
            work_data = None
    
    except Exception as e:
        print(f"An error occurred: {e}")
        work_data = None
    
    finally:
        cur.close()
        conn.close()
    
    return work_data

def updateWork(work_id, title, course, description, price):
    conn = connect()
    cur = conn.cursor()

    try:
        query = """
            UPDATE "work"
            SET title = %s,
                course = %s,
                description = %s,
                price = %s
            WHERE id = %s;
        """
        
        cur.execute(query, (title, course, description, price, work_id))
        conn.commit()

        if cur.rowcount > 0:
            return True
        else:
            return False
    
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    
    finally:
        cur.close()
        conn.close()

def deleteWork(work_id):
    conn = connect()
    cur = conn.cursor()
    
    try:
        query = """
            DELETE FROM "work"
            WHERE id = %s;
        """
        
        cur.execute(query, (work_id,))
        conn.commit()  # Confirma as alterações no banco de dados
        
        # Verifica se a exclusão foi realizada com sucesso
        if cur.rowcount > 0:
            return True
        else:
            return False
    
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()  # Reverte as alterações em caso de erro
        return False
    
    finally:
        cur.close()
        conn.close()


def getCourses():
    conn = connect()
    cur = conn.cursor()
    
    try:
        cur.execute("SELECT * FROM \"course\";")
        works = []
        for work in cur.fetchall():
            works.append({
                'id': work[0],
                'title': work[1],
                'teacher': work[2],
            })
        
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        cur.close()
        conn.close()
    
    return works