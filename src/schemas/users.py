from pydantic import BaseModel, ConfigDict, EmailStr


class UserAdd(BaseModel):
    email: EmailStr
    hashed_password: str
    firstname: str
    lastname: str
    nickname: str

class UserRequestAdd(BaseModel):
    email: EmailStr
    password: str
    firstname: str
    lastname: str
    nickname: str

class User(BaseModel):
    id: int
    email: EmailStr
    firstname: str
    lastname: str
    nickname: str

    model_config = ConfigDict(from_attributes=True)

