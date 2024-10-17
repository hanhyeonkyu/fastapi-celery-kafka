from fastapi import FastAPI
from celery import Celery
from kombu import Exchange, Queue

app = FastAPI()

# Celery 설정
celery = Celery(
    "tasks",
    broker="kafka://kafka:9092",  # Kafka 브로커
    backend="redis://redis:6379/0",  # Redis 백엔드
)

# Kafka 브로커를 위한 Celery 설정
celery.conf.task_queues = (
    Queue("default", Exchange("default", type="direct"), routing_key="default"),
)

celery.conf.task_default_queue = "default"
celery.conf.task_default_exchange = "default"
celery.conf.task_default_exchange_type = "direct"
celery.conf.task_default_routing_key = "default"

# Kafka transport 옵션 추가
celery.conf.broker_transport_options = {
    "acks": "all",  # 메시지가 안전하게 전송되었는지 확인
    "compression": "gzip",  # 메시지 압축
    "group.id": "celery-group",  # Kafka 그룹 ID
    "auto.offset.reset": "earliest",  # 브로커 초기화 옵션
}


@celery.task
def background_task(data):
    return f"Processed {data}"


@app.get("/")
async def home():
    return "Hello, This is fastapi app!"


@app.get("/proc")
async def proc():
    task = background_task.delay("hello celery!")
    return {"task_id": task.id}


@app.post("/process")
async def process(data: str):
    task = background_task.delay(data)
    return {"task_id": task.id}
