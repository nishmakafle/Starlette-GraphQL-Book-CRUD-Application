from starlette.applications import Starlette
import strawberry
from models import session
import typing
from userapp.models import User, UserProfile
from userapp.schema import UserSchema
from .helpers import hash_password


def get_user() -> UserSchema:
    users = results = session.query(User).all()
    return users


@strawberry.type
class Query:
    users: typing.List[UserSchema] = strawberry.field(resolver=get_user)


@strawberry.type
class Mutation:
    @strawberry.mutation
    def register_user(self, username:str, password:str, email:str) ->UserSchema:
        hpassword = hash_password(password)
        
        try:  
            user = User(username=username, password=str(hash_password), email=email)
            session.add(user)   
            session.commit()
        except:
            session.rollback()
            raise
        return user



user_schema = strawberry.Schema(query=Query, mutation=Mutation)