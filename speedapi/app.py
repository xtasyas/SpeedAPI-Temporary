from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from speedapi.schemas import (
    Message,
    UserDB,
    UserPrivate,
    UserPublic,
    UsersList,
)

app = FastAPI(debug=True)


database = []


# This decorator is refered as 'Path Operation Decorator'
# Endpoints are functions avaliabe through the API
# Routes are the URL used to acess those endpoints
# '/' is the route template
# Function return is the endpoint resource
@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Welcome to SpeedAPI!'}


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserPrivate):
    user_db = UserDB(id=len(database) + 1, **user.model_dump())

    for any_user in database:
        if any_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='User already exists.',
            )

    database.append(user_db)

    return user_db


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UsersList)
def read_users():
    return {'users': database}


@app.put(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPrivate
)
def update_user(user_id: int, user: UserPrivate):
    if user_id == 0 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not exists.'
        )

    updated_user = UserDB(id=user_id, **user.model_dump())
    database[user_id - 1] = updated_user

    return updated_user

@app.delete(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=Message
)
def delete_user(user_id: int):
    if user_id == 0 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not exists.'
        )

    del database[user_id - 1]

    return {'message': f'User with ID {user_id} has been deleted.'}
