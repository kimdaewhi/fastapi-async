from fastapi import FastAPI
import time
import threading

app = FastAPI()

# Start-Job { Invoke-WebRequest http://127.0.0.1:8000/sync } 테스트
@app.get("/sync")
def sync():
    tid = threading.get_ident()

    print(f"Hello {tid}")
    time.sleep(2)
    print(f"Bye {tid}")