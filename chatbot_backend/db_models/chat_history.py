from ..connect_db import conn

def fetch_recent_messages(user_id: int, limit: int = 100):
    """
    Returns:
    - None                → if user has no history
    - List of messages    → if history exists
    """

    with conn.cursor() as cur:
        # Count messages
        cur.execute(
            "SELECT COUNT(*) FROM chat_history WHERE user_id=%s;",
            (user_id,)
        )
        total = cur.fetchone()[0]

        # No history
        if total == 0:
            return []

        # Decide limit
        fetch_limit = limit if total >= limit else total

        # Fetch messages (latest first)
        cur.execute(
            """
            SELECT role, message
            FROM chat_history
            WHERE user_id=%s
            ORDER BY id DESC
            LIMIT %s;
            """,
            (user_id, fetch_limit)
        )

        rows = cur.fetchall()
 
    return list(reversed(rows))




    