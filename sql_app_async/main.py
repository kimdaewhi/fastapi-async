from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sql_app_async import models, schemas, database

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.database.disconnect()

# 비동기 DB 세션을 의존성 주입으로 사용
@app.get("/notes/", response_model=List[schemas.Note])
async def read_notes(skip: int = 0, limit: int = 10, db = Depends(database.get_db)):
    query = models.Note.__table__.select().offset(skip).limit(limit)
    notes = await db.fetch_all(query)  # 비동기 처리
    return notes

@app.post("/notes/", response_model=schemas.Note)
async def create_note(note: schemas.NoteCreate, db = Depends(database.get_db)):
    query = models.Note.__table__.insert().values(text=note.text, completed=note.completed)
    last_record_id = await db.execute(query)  # 비동기 처리
    return {**note.model_dump(), "id": last_record_id}
