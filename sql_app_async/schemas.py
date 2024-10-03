from pydantic import BaseModel, ConfigDict

class NoteBase(BaseModel):
    text: str
    completed: bool
    
class NoteCreate(NoteBase):
    pass

class Note(NoteBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)