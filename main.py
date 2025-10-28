from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import os

app = FastAPI(title="CLG Backend API", version="0.1.0")

# --- CORS setup ---
origins = [
    "http://127.0.0.1:3000",  # local frontend (Next.js dev)
    "http://localhost:3000",
    "https://aiagentclg.com",  # your live domain
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# -------------------

@app.get("/")
def root():
    return {"status": "CLG API running"}

@app.get("/health")
def health_check():
    return {"ok": True, "timestamp": datetime.now()}

@app.post("/generate_qapi")
def generate_qapi():
    os.makedirs("output", exist_ok=True)
    filename = f"output/QA_PI_Summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, "w") as f:
        f.write("QA/PI Summary generated successfully.\n")
        f.write(f"Timestamp: {datetime.now()}\n")
    return {"message": f"Created {filename}"}

@app.on_event("shutdown")
def shutdown_event():
    print("🧹 Shutting down CLG backend cleanly.")

