from fastapi import FastAPI
import time
import threading
import asyncio

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