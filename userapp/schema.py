import typing
import strawberry


@strawberry.type
class UserSchema:
    id : strawberry.ID
    username : str
    password : str
    email : str

@strawberry.type
class UserProfileSchema:
    id : strawberry.ID
    firstname : str
    lastname : str
    address : str
    image : str
    phone_number : str
    dob : str
    user : UserSchema