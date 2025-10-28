# CLG-App  
Backend engine for AI Agent CLG — automating licensing, certification, and compliance workflows for behavioral health and treatment programs.

## Run locally
```bash
source venv/bin/activate
uvicorn main:app --reload
```

Then open http://127.0.0.1:8000/docs for interactive API documentation.

## Routes
- GET / — Root
- GET /health — Health check
- POST /generate_qapi — Generate QAPI report

## Author
Brian Burgess | AI Agent CLG

