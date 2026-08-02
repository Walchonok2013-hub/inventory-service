from pydantic import BaseModel, EmailStr
from pydantic import ConfigDict
class UserCreate(BaseModel):
    username: str 
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    username: str  
    id: int
    email: str

    # Правильный синтаксис для Pydantic V2
    model_config = ConfigDict(from_attributes=True)