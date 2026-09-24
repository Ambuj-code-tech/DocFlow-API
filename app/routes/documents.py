from starlette.responses import JSONResponse        #this lets us send JSON back to whoever called our API
from starlette.templating import Jinja2Templates

from app.database.database import SessionLocal
from app.models.document import Document


templates = Jinja2Templates(directory="templates")


async def documents(request):
    db = SessionLocal()

    try:
        documents = db.query(Document).all()

        return JSONResponse({
            "documents": [
                {
                    "id": document.id,
                    "filename": document.filename,
                    "status": document.status,
                    "created_at": document.created_at.isoformat()
                }
                for document in documents
            ]
        })

    finally:
        db.close()

async def document(request):
    document_id = request.path_params["id"]

    db = SessionLocal()

    try:
        document = db.get(Document, int(document_id))       # SELECT * FROM documents WHERE id = {{document_id}};

        if document is None:
            return JSONResponse(
                {
                    "error": "Document not found"
                },
                status_code=404
            )

        return JSONResponse({
            "document_id": document.id,
            "status": document.status,
            "filename": document.filename,
            "created_at": document.created_at.isoformat()
        })

    finally:
        db.close()

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

    db = SessionLocal()

    try:
        document = Document(
            filename=filename,
            status="processing"
        )

        db.add(document)
        db.commit()
        db.refresh(document)

        return JSONResponse(
            {
                "message": "Document created",
                "document": {
                    "id": document.id,
                    "filename": document.filename,
                    "status": document.status,
                    "created_at": document.created_at.isoformat()
                }
            },
            status_code=201
        )

    finally:
        db.close()

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