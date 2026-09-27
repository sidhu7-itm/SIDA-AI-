from pydantic import BaseModel


# Used when creating a new user
class UserCreate(BaseModel):
    username: str
    email: str
    password: str


# Used when logging in
class UserLogin(BaseModel):
    username: str
    password: str


# Used when the API returns user data
class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True