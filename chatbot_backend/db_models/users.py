from ..connect_db import conn


##SignUp Function For database
def signup_user(username: str, password: str):

    with conn.cursor() as cur:
        try:
            cur.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s);",
                (username, password)
            )
            conn.commit()
            return True, "User created successfully"
        except Exception:
            conn.rollback()
            return False, "Username already exists"
        
        
# Login function For database
def login_user(username: str, password: str):
    with conn.cursor() as cur:
        cur.execute(
            "SELECT id, password FROM users WHERE username = %s;",
            (username,)
        )
        result = cur.fetchone()

        if result is None:
            return False, "Username does not exist", None

        user_id, stored_password = result
        current_id=user_id
        if stored_password == password:
            return True, "Login successful", user_id
        else:
            return False, "Incorrect password", None

        
