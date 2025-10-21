from fastapi import FastAPI,Depends,status,Response,HTTPException
import schemas, models
from database import engine,SessionLocal
from typing import List
from sqlalchemy.orm import Session
from passlib.context import CryptContext


app=FastAPI()
models.Base.metadata.drop_all(engine)
models.Base.metadata.create_all(engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/blog",tags=['blogs'])
def create_blog(request:schemas.Blog,db:Session=Depends(get_db)):
    new_blog=models.Blog(title=request.title,body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get("/blog",response_model=List[schemas.ShowBlog],tags=['blogs'])
def all(db:Session=Depends(get_db)):
    blogs=db.query(models.Blog).all()
    return blogs

@app.get("/blog/{id}",status_code=200,response_model=schemas.ShowBlog,tags=['blogs'])
def getbyid(id,response:Response,db:Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="blog with id no. {id} is not available in database")
       
    return blog

@app.delete("/blog/{id}",status_code=status.HTTP_204_NO_CONTENT,tags=['blogs'])

def destroy(id,db:Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="blog record is not present in database")
    blog.delete(synchronize_session=False)
    db.commit()
    return "done"

@app.put("/blog/{id}",status_code=status.HTTP_202_ACCEPTED,tags=['blogs'])
def up(id,request:schemas.Blog,db:Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="detail with id {id} not found")
    blog.update({'title':'updated title'})
    db.commit()
    return "updated"

pwd_Context=CryptContext(schemes=['bcrypt'],deprecated="auto")
@app.post("/user",response_model=schemas.ShowUser,tags=['users'])
def createuser(request:schemas.User,db:Session=Depends(get_db)):
    hashed_pass=pwd_Context.hash(request.password[:72])
    new_user=models.User(name=request.name,password=hashed_pass,email=request.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/user/{id}",response_model=schemas.ShowUser,tags=['users'])
def showuser(id:int,db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user with id {id} not found")
    return user