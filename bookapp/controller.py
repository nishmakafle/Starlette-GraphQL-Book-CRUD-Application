
import typing

import strawberry
from sqlalchemy import desc


from bookapp.models import BookDB, CategoryDB, Tag
from bookapp.schema import Book, Category, CategoryDetail, TagSchema, BookFilterByTag
from models import session


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

def get_books_by_tag(self, tag_id:strawberry.ID)->Book:
    results = session.query(BookDB).filter(BookDB.tag.any(id=tag_id)).all()
    return results

@strawberry.type
class Query:
    categories: typing.List[Category] = strawberry.field(resolver=get_categories)
    books:typing.List[Book] = strawberry.field(resolver=get_books)
    tags:typing.List[TagSchema] = strawberry.field(resolver=get_tags)
    tag_books:typing.List[Book] = strawberry.field(resolver=get_books_by_tag) ## Book filter by tag

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

    @strawberry.mutation
    def update_book(self,book_id:int, category_id:int, name:str, author:str, description:str, quantity:int, tags:list[int])->Book:

        obj = session.query(BookDB).get(book_id)
        if obj:
            category=get_objects(category_id)
            tags = session.query(Tag).filter(Tag.id.in_(tags)).all()
            obj.name = name
            obj.description = description
            obj.author = author
            obj.quantity = quantity
            obj.tag = tags
            session.commit()
        else:
            return CustomError(f"Object Does not exit")
        return obj

#............. For Tags......................

    @strawberry.mutation
    def add_tag(self, name:str) -> TagSchema:
        tag = Tag(name=name)
        session.add(tag)
        session.commit()
        return tag



bookapp_schema = strawberry.Schema(query=Query, mutation=Mutation)
