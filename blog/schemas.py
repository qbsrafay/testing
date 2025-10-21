from pydantic import BaseModel

class Blog(BaseModel):
    title: str
    body: str

class ShowBlog(Blog):
    title: str  # ye line optional hai, kyunki parent class me already hai
    class Config:
        orm_mode = True
        

class User(BaseModel):
    password:str
    email:str
    name:str

class ShowUser(BaseModel):
    email:str
    name:str
    class Config:
        orm_mode = True