import typing
from datetime import date

import strawberry


@strawberry.type
class Category:
    id:strawberry.ID
    title:str


@strawberry.type
class TagSchema:
    id:strawberry.ID
    name:str


@strawberry.type
class Book:
    id:strawberry.ID
    name:str
    author:str
    description:str
    category:Category
    quantity:int
    tag:list[TagSchema]


@strawberry.type
class CategoryDetail:
    id:strawberry.ID
    title:str
    book:Book

@strawberry.type
class BookFilterByTag:
    id:strawberry.ID
    name:str
    author:str
    description:str
    category:Category
    quantity:int