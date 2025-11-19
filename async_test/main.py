from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Optional, Literal
import time
import threading
import asyncio
import uvicorn
import uuid

app = FastAPI()

# Start-Job { Invoke-WebRequest http://127.0.0.1:8000/sync }
@app.get("/sync")
def sync():
    tid = threading.get_ident()

    print(f"Hello {tid}")
    time.sleep(1)
    print(f"Bye {tid}")



# Start-Job { Invoke-WebRequest http://127.0.0.1:8000/async }
@app.get("/async")
async def sync():
    tid = threading.get_ident()

    print(f"Hello {tid}")
    await asyncio.sleep(1)
    print(f"Bye {tid}")


class OrderCreate(BaseModel):
    symbol: str = Field(..., example="AAPL")
    side: Literal["buy", "sell"]
    quantity: int = Field(..., gt=0, example=10)
    price: float = Field(..., gt=0, example=190.5)


class Order(OrderCreate):
    id: str
    status: Literal["pending", "filled", "canceled"]


ORDERS: dict[str, Order] = {}

@app.post("/orders", response_model=Order)
async def create_order(order_in: OrderCreate):
    order_id = str(uuid.uuid4())
    
    order = Order(
        id=order_id,
        status="pending",
        **order_in.model_dump(),
    )
    
    ORDERS[order_id] = order
    
    await asyncio.sleep(0.3)
    
    order.status = "filled"
    
    return order


@app.get("/orders/{order_id}", response_model=List[Order])
async def get_order(order_id: str):
    order = ORDERS.get(order_id)
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return order


@app.get("/orders", response_model=List[Order])
async def list_orders(status: Optional[Literal["pending", "filled", "canceled"]] = Query(default=None), min_qty: Optional[int] = Query(default=None, gt=1)):
    result = list(ORDERS.values())
    
    if status:
        result = [o for o in result if o.status == status]
    
    if min_qty is not None:
        result = [o for o in result if o.quantity >= min_qty]
    
    result.sort(key=lambda o: o.quantity, reverse=True)
    return result


# 실행 : python main:a
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)