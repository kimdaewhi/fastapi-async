import databases
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from .models import Base

DATABASE_URL = f"postgresql://postgres:1q2w3e4r!!@localhost:5432/postgres"

engine = sqlalchemy.create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 비동기 데이터베이스 연결
database = databases.Database(DATABASE_URL)

def init_db():
    Base.metadata.create_all(bind=engine)

# 비동기용 get_db 함수 추가
async def get_db():
    try:
        if not database.is_connected:
            await database.connect()
        yield database
    finally:
        await database.disconnect()
