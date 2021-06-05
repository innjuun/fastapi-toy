from typing import Optional

import uvicorn
import pickle
from fastapi import FastAPI
from pydantic import BaseModel
from redis_client import redis_client, redis_cluster_client


app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int):
    response = pickle.loads(redis_cluster_client.get(item_id))
    return {"item": response}

@app.get("/cpu-work")
def cpu_work():
    for x in range(1000000):
        a = x*x*x*x
    return {"work": "done"}

@app.post("/items/{item_id}")
def update_item(item_id: int, item: Item):
    redis_cluster_client.set(name=item_id, value=pickle.dumps(item))
    return {"item_name": item.name, "item_id": item_id}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)