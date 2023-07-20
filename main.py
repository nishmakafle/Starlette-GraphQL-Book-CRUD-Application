
import typing

import strawberry
from sqlalchemy import desc
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from strawberry.asgi import GraphQL

from models import BookDB, CategoryDB, Tag, session
from schema import Book, Category, CategoryDetail, TagSchema


class CustomError(Exception):
    def __init__(self, message: str):
        self.message = message


def get_categories() -> typing.List[Category]:
    results = session.query(CategoryDB).order_by(desc(CategoryDB.id)).all()
    return results


def get_books() ->Book:
    results = session.query(BookDB).all()
    return results

def get_objects(id):
    data = session.query(CategoryDB).get(id)
    if data:
        return data
    else:
        return CustomError(f"Object Does not exit")

def get_tags() -> TagSchema :
    tags = session.query(Tag).all()
    return tags 

@strawberry.type
class Query:
    categories: typing.List[Category] = strawberry.field(resolver=get_categories)
    books:typing.List[Book] = strawberry.field(resolver=get_books)
    tags:typing.List[TagSchema] = strawberry.field(resolver=get_tags)

    @strawberry.field
    def get_category_detail(self, category_id: strawberry.ID) -> CategoryDetail:
        data = session.query(CategoryDB).filter(CategoryDB.id == category_id).one()
        return data
        

    


@strawberry.type
class Mutation:

    @strawberry.mutation
    def add_category(self, title:str) -> Category:
        cat = CategoryDB(title=title)
        session.add(cat)
        session.commit()
        return cat

    @strawberry.mutation
    def update_category(self,id:int, title:str)->Category:
        obj = session.query(CategoryDB).get(id)
        if obj:
            obj.title = title
            session.commit()
        else:
            return CustomError(f"Object Does not exit")
        return obj

    @strawberry.mutation
    def delete_category(self, id:int)->Category:
        obj = session.query(CategoryDB).get(id)
        if obj:
            session.delete(obj)
            session.commit()
        else:
            return CustomError(f"Object does not found with ID {id}")
        return CustomError(f" Category deleted Successfully")

#........... For Book ...............
    @strawberry.mutation
    def add_book(self,category_id:int, name:str, author:str, description:str, quantity:int, tags:list[int]) -> Book:
        category=get_objects(category_id)
        tags = session.query(Tag).filter(Tag.id.in_(tags)).all()
        book = BookDB(category_id=category.id, name=name, author=author, description=description, quantity=quantity, tag=tags)
        session.add(book)
        session.commit()
        return book

#............. For Tags......................

    @strawberry.mutation
    def add_tag(self, name:str) -> TagSchema:
        tag = Tag(name=name)
        session.add(tag)
        session.commit()
        return tag



schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQL(schema)
app = Starlette()
app.add_route("/graphql", graphql_app)