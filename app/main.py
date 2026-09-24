from starlette.applications import Starlette    #import main starlette application class
from starlette.routing import Route             #Route connects a url to a pthon function
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles

from app.routes.documents import (
    documents,
    document,
    create_document,
    upload_document,
)

from app.database.database import engine
from app.models.document import Base


Base.metadata.create_all(bind=engine)


templates = Jinja2Templates(directory="templates")


async def homepage(request):    #python function that starlette will execute when someone access '/'
    return templates.TemplateResponse(
        request,
        "index.html"
    )


routes = [
    Route('/', homepage),
    Route('/documents', documents),
    Route('/documents', create_document, methods=["POST"]),
    Route('/documents/upload', upload_document, methods=["POST"]),
    Route('/documents/{id}', document)  #{id} is a path parameter
]


app = Starlette(routes=routes)


app.mount(
    "/static", 
    StaticFiles(directory="static"), 
    name="static"
)