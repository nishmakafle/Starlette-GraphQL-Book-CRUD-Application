from starlette.applications import Starlette
import strawberry
from models import session
import typing
from userapp.models import User, UserProfile
from userapp.schema import UserSchema, UserProfileSchema
from .helpers import hash_password, CustomError



def get_objects(id):
    data = session.query(User).get(id)
    if data:
        return data
    else:
        return CustomError(f"Object Does not exit")


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

    @strawberry.mutation
    def create_profile(self, firstname:str, lastname:str, address:str, phone_number:str, dob:str, user_id:int) ->UserProfileSchema:
        user = get_objects(user_id)
        try:
            user_profile = UserProfile(firstname=firstname, lastname=lastname, address=address, phone_number=phone_number, dob=dob, user_id=user.id)
            session.add(user_profile)
            session.commit()
        except:
            session.rollback()
            raise
            
        return user_profile




user_schema = strawberry.Schema(query=Query, mutation=Mutation)