from fastapi import FastAPI
from preprocess import process_data
from db import save_to_db, create_table, get_connection
from fastapi.responses import HTMLResponse
import json
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 🔥 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 🔥 CREATE TABLE ON START
@app.on_event("startup")
def startup():
    create_table()
    print("✅ Table ready")


# 🔥 HOME
@app.get("/")
def home():
    return {"message": "Backend running 🚀"}


# 🔥 RECEIVE DATA FROM N8N
@app.post("/receive-data")
def receive_data(data: dict):
    print("🔥 Received:", data)

    processed = process_data(data)

    if not processed:
        return {"status": "no data received"}

    save_to_db(processed)

    return {
        "status": "stored in DB",
        "processed_data": processed
    }


# 🔥 GET PROCESSED DATA
@app.get("/processed-data/{user_id}")
def get_processed_data(user_id: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT user_id, platform, cleaned_text, timestamps, metadata, ml_output
        FROM processed_data
        WHERE user_id = %s
        ORDER BY id DESC
        LIMIT 1
    """, (user_id,))

    row = cur.fetchone()

    cur.close()
    conn.close()

    if not row:
        return {"status": "no data"}

    return {
        "user_id": row[0],
        "platform": row[1],
        "cleaned_text": row[2],
        "timestamps": row[3],
        "metadata": row[4],
        "ml_output": row[5]
    }


# 🔥 RECEIVE FINAL OUTPUT FROM ML + LLM
@app.post("/final-output")
def receive_final_output(data: dict):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE processed_data
        SET ml_output = %s
        WHERE user_id = %s
    """, (
        json.dumps(data),
        data["user_id"]
    ))

    conn.commit()
    cur.close()
    conn.close()

    return {"status": "final output stored"}



# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from db import insert_data, get_data
# import json

# app = FastAPI()

# # 🔥 CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# @app.post("/receive-data")
# def receive_data(payload: dict):
#     user_id = payload["user_id"]
#     platform = payload["platform"]

#     # 🔥 Skip preprocess, use raw payload directly
#     processed = {
#         "user_id": user_id,
#         "platform": platform,
#         "text": payload.get("text", ""),
#         "ml_output": {
#             "ocean": {
#                 "openness": 0.7,
#                 "conscientiousness": 0.6,
#                 "extraversion": 0.5,
#                 "agreeableness": 0.8,
#                 "neuroticism": 0.3
#             },
#             "confidence": 0.85,
#             "explanation": "User is balanced and analytical."
#         }
#     }

#     insert_data(user_id, platform, processed)

#     return {"status": "stored"}


# @app.get("/processed-data/{user_id}")
# def get_processed(user_id: str):
#     data = get_data(user_id)
#     return data
# @app.post("/receive-data")
# def receive_data(payload: dict):
#     print("🔥 RAW PAYLOAD FROM N8N:", payload)  # 👈 this will show everything
#     return {"status": "received"}