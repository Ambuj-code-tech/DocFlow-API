from starlette.applications import Starlette    #import main starlette application class
from starlette.responses import JSONResponse    #this lets us send JSON back to whoever called our API
from starlette.routing import Route             #Route connects a url to a pthon function
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles

valid_ids = [
    "42",
]

templates = Jinja2Templates(directory="templates")

async def homepage(request):    #python function that starlette will execute when someone access '/'
    return templates.TemplateResponse(
        request,
        "index.html"
    )

async def documents(request):
    return JSONResponse({
        "documents": [
            "report.txt",
            "research.pdf",
            "presentation.docx"
        ]
    })

async def document(request):
    document_id = request.path_params['id']

    if document_id in valid_ids:
        return JSONResponse({
            "document_id": document_id,
            "status": "completed",
            "filename": "report.pdf"
        })

    else:
        return JSONResponse(
            {
                "error": "Document not found"
            },
            status_code=404
        )

async def create_document(request):
    #Read the JSON body sent by the client, wait for it to be available, convert it into a Python object, and store that object in data.
    data = await request.json()

    if "filename" not in data:
        return JSONResponse(
            {
                "error": "filename is required"
            },
            status_code=400
        )

    filename = data["filename"]

    if not filename:
        return JSONResponse(
            {
                "error": "filename cannot be empty"
            },
            status_code=400
        )

    return JSONResponse({
        "message": "Document received",
        "filename": filename,
    })

async def upload_document(request):
    form = await request.form()

    file = form["file"]

    contents = await file.read()

    return templates.TemplateResponse(
        request,
        "result.html",
        {
            "filename": file.filename,
            "size": len(contents)
        }
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