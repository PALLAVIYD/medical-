from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email:str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

# Pydantic model for receiving form data
class MoodData(BaseModel):
    mood_description: str
    mood: str
