from starlette.applications import Starlette
from starlette.routing import Mount, Route
from bookapp.controller import bookapp_schema

from strawberry.asgi import GraphQL



app = Starlette()

app.mount("/book_app", GraphQL(bookapp_schema))