# DocFlow API

A full-stack document processing API built with Python and Starlette, featuring file uploads, validation, server-side HTML rendering, and a simple web interface.

## Current Features
- Document Upload
- Document Management
- Document Versioning
- Text Extraction
- Document Search
- Background Job Processing
- Database
- Authentication & Authorization
- Rate Limiting
- Caching
- Proper Error Handling
- Pagination & Filtering
- API Documentation
- Testing
- Docker & Deployment

## Project Structure

```text
DocFlowAPI/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   └── documents.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── document.py
│   │
│   └── database/
│       ├── __init__.py
│       └── database.py
│
├── templates/
├── static/
├── uploads/
│
├── README.md
├── .gitignore
└── requirements.txt
