from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from speedapi.database import get_session
from speedapi.models import User
from sqlalchemy import select
from sqlalchemy.orm import Session

from speedapi.schemas import Message, UserPrivate, UserPublic, UsersList

app = FastAPI(debug=True)


# This decorator is refered as 'Path Operation Decorator'
# Endpoints are functions avaliabe through the API
# Routes are the URL used to acess those endpoints
# '/' is the route template
# Function return is the endpoint resource
@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Welcome to SpeedAPI!'}


@app.post('/users/',
          status_code=HTTPStatus.CREATED,
          response_model=UserPublic)
def create_user(user: UserPrivate, session: Session = Depends(get_session)):
    verify_user_in_database = session.scalar(


        select(User).filter_by(
            username=user.username,
            email=user.email

        )
    )

    if verify_user_in_database:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='User already exists.',
        )

    session.add(new_user := User(**user.model_dump()))
    session.commit()
    session.refresh(new_user)

    return new_user


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UsersList)
def read_users(
    offset: int = 0, limit: int = 10, session: Session = Depends(get_session)
):
    users = session.scalars(select(User).limit(limit).offset(offset)).all()

    return {'users': users}


@app.put('/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPrivate)
def update_user(
    user_id: int, user: UserPrivate, session: Session = Depends(get_session)
):
    user_to_be_updated = session.get(entity=User, ident=user_id)

    if user_to_be_updated is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not exists.'
        )

    for attribute in ('username', 'email', 'password'):
        setattr(user_to_be_updated, attribute, getattr(user, attribute))

    session.add(user_to_be_updated)
    session.commit()

    return user_to_be_updated


@app.delete('/users/{user_id}', status_code=HTTPStatus.OK, response_model=Message)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user_to_be_deleted = session.get(entity=User, ident=user_id)

    if user_to_be_deleted is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not exists.'
        )

    session.delete(user_to_be_deleted)
    session.commit()

    return {'message': f'User with ID {user_id} has been deleted.'}
