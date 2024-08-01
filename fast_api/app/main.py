from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google.cloud import pubsub_v1
import os,json

app = FastAPI()

# CORS設定
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:9000",
    "http://example.com",  # 特定のオリジンを追加
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 許可するオリジンを指定
    allow_credentials=True,
    allow_methods=["*"],  # 許可するHTTPメソッドを指定
    allow_headers=["*"],  # 許可するHTTPヘッダーを指定
)

@app.get("/")
def read_root():
    return {"Hello!!": "World!!!"}


# Google Cloud Pub/Subの設定
publisher = pubsub_v1.PublisherClient()
project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
topic_id = os.getenv('TOPIC_NAME')  # 適切なトピック名に設定してください

topic_name = f'projects/{project_id}/topics/{topic_id}'

# Pydanticモデルを使用してリクエストボディの構造を定義
class Message(BaseModel):
    spam: str
    message: str
    data: str


@app.post("/publish")
async def publish_message(message: Message):
    try:
        # メッセージをPub/Subに送信
        future = publisher.publish(
            topic_name,
            message.json().encode('utf-8')
        )
        # メッセージ送信の結果を取得
        future.result()
        return {"status": "Message published successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
