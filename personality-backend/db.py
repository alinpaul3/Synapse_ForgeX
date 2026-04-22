import psycopg2
import json

def get_connection():
    return psycopg2.connect(
        dbname="personality_db",
        user="postgres",
        password="Truepacer@3253",
        host="localhost",
        port="5432"
    )


def create_table():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS processed_data (
            id SERIAL PRIMARY KEY,
            user_id TEXT,
            platform TEXT,
            cleaned_text JSONB,
            timestamps JSONB,
            metadata JSONB,
            ml_output JSONB
        )
    """)

    conn.commit()
    cur.close()
    conn.close()


def save_to_db(data):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO processed_data 
        (user_id, platform, cleaned_text, timestamps, metadata)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        data["user_id"],
        data["platform"],
        json.dumps(data["cleaned_text"]),
        json.dumps(data["timestamps"]),
        json.dumps(data["metadata"])
    ))

    conn.commit()
    cur.close()
    conn.close()



# import psycopg2
# from psycopg2.extras import Json

# def get_connection():
#     return psycopg2.connect(
#         dbname="personality_db",
#         user="postgres",
#         password="Truepacer@3253",
#         host="localhost",
#         port="5432"
#     )

# def insert_data(user_id, platform, data):
#     conn = get_connection()
#     cur = conn.cursor()

#     cur.execute("""
#         INSERT INTO processed_data (user_id, platform, ml_output)
#         VALUES (%s, %s, %s)
#     """, (user_id, platform, Json(data)))

#     conn.commit()
#     cur.close()
#     conn.close()


# def get_data(user_id):
#     conn = get_connection()
#     cur = conn.cursor()

#     cur.execute("""
#         SELECT ml_output FROM processed_data
#         WHERE user_id=%s
#         ORDER BY id DESC LIMIT 1
#     """, (user_id,))

#     row = cur.fetchone()
#     cur.close()
#     conn.close()

#     return row[0] if row else {}