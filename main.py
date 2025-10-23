from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel


app = FastAPI()

@app.get('/')
async def read_root():
    return {'message': 'Hello WOrld!'}


@app.get('/greet/{name}')
async def say_hello(name:Optional[str] = 'User', age:int=0)-> dict:
    return {'message': f'Hello {name}', 'age': age}


class BookCreateModel(BaseModel):
    title: str
    author: str




@app.post('/create_book')
async def create_book(book_data: BookCreateModel):
    return {
        'title': book_data.title,
        'author': book_data.author
    }