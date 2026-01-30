from ..connect_db import conn

## Save messages to DB
def save_message(user_id: int, role: str, message: str):
    """
    Save a single chat message (human or ai) into database
    """

    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO chat_history (user_id, role, message)
            VALUES (%s, %s, %s);
            """,
            (user_id, role, message)
        )
        conn.commit()

# id=1
# r="ai"
# m="I am AI assistant?"

# ok=save_message(id, r, m)
# print("OK",ok)
