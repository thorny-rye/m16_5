from fastapi import FastAPI, HTTPException, Body, Request, Path
from pydantic import BaseModel
from typing import List, Annotated
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

templates = Jinja2Templates(directory="templates")
app = FastAPI()

users = []


class User(BaseModel):
    id: int = None
    username: str
    age: int = None


@app.get('/')
async def get_query(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('users.html', {"request": request, "users": users})

@app.get('/user/{user_id}')
async def get_query2(
        request: Request,
                     user_id:
                     Annotated[int, Path(ge=1, le=100, description='Enter User ID', example='1')]) -> HTMLResponse:
    try:
        for user in users:
            if user.id == user_id:
                return templates.TemplateResponse("users.html", {"request": request, "user": users[user_id-1]})
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")



@app.post('/user/{username}/{age}')
async def post_query(
        username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username', example='UrbanUser')],
                    age: Annotated[int, Path(ge=18, le=120, description='Enter age', example='24')]):
    new_id = users[-1].id + 1 if users else 1
    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user)
    return new_user


@app.put('/user/{user_id}/{username}/{age}')
async def put_query(user_id: Annotated[int, Path(ge=1, le=100,description="Specify User ID", examples=[1])],
                    username: Annotated[str, Path(min_length=5, max_length=20,
                                                  description="Input your username", examples=["Marcus"])],
                    age: Annotated[int, Path(ge=18, le=120, description="Input your age", examples=[22])]) -> str:
    try:
        edit_id = users[user_id]
        edit_id.username = username
        edit_id.age = age
        return edit_id
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")


@app.delete('/user/{user_id}')
async def delete_query(user_id:
Annotated[int, Path(ge=0, le=100,description="Specify User ID which would deleted", examples=[1])],
                       user: User) -> List[User]:
    try:
        del_user = users[user_id]
        users.pop(del_user)
        return user
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")
