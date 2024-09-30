from pydantic import BaseModel, ConfigDict

# Item Base Model 만들기
class ItemBase(BaseModel):
    title: str
    description: str | None = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    owner_id: int
    
    # pydantic의 Config는 다음과 같은 효과를 가진다
    # id = data.id
    # title = data.title
    # description = data.description .....
    # class Config:
    #     orm_mode = True
    model_config = ConfigDict(from_attributes=True)



# lazy loading?
class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []

    # class Config:
    #     orm_mode = True
    model_config = ConfigDict(from_attributes=True)