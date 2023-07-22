import typing
import strawberry


@strawberry.type
class UserSchema:
    id : strawberry.ID
    username : str
    password : str
    email : str