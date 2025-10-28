from fastapi import FastAPI
from config import APP_NAME, VERSION, DESCRIPTION, AUTHOR

app = FastAPI(
    title=APP_NAME,
    version=VERSION,
    description=DESCRIPTION
)

@app.get("/")
def root():
    return {"status": "CLG API running"}

@app.get("/health")
def health_check():
    return {"health": "ok"}

@app.get("/info")
def app_info():
    return {
        "app_name": APP_NAME,
        "version": VERSION,
        "author": AUTHOR
    }

@app.post("/generate_qapi")
def generate_qapi():
    # Placeholder for your QAPI logic
    return {"message": "QAPI generation endpoint is ready"}

import os
import json

@app.get("/audit")
def run_audit():
    """Scan local compliance data and summarize status."""
    output_dir = os.path.expanduser("~/Desktop/XM4-LabTwin")
    summary = {"files_found": [], "report_summary": {}}

    try:
        for file in os.listdir(output_dir):
            if file.endswith(".json") or file.endswith(".csv"):
                summary["files_found"].append(file)

        latest_json = sorted(
            [f for f in summary["files_found"] if f.startswith("XM4_Model_Report")],
            reverse=True
        )

        if latest_json:
            latest_path = os.path.join(output_dir, latest_json[0])
            with open(latest_path, "r") as f:
                data = json.load(f)

            # Try to extract common keys
            compliance_score = None
            key_findings = []
            for k, v in data.items():
                if isinstance(v, (int, float)) and "score" in k.lower():
                    compliance_score = v
                if isinstance(v, str) and any(x in v.lower() for x in ["risk", "missing", "flag"]):
                    key_findings.append(v)

            summary["report_summary"] = {
                "latest_report": latest_json[0],
                "overall_compliance": compliance_score if compliance_score else "N/A",
                "key_findings": key_findings[:5] if key_findings else ["No risk findings detected."]
            }
        else:
            summary["report_summary"] = {"message": "No XM4 reports found."}

    except Exception as e:
        summary["error"] = str(e)

    return summary
from fastapi import UploadFile, File
from pathlib import Path

UPLOAD_DIR = Path.home() / "CLG-App" / "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/licensing/apply")
async def upload_licensing_docs(file: UploadFile = File(...)):
    """Upload DHCS or certification documents and auto-sort by category."""
    filename = file.filename.lower()

    if "6040" in filename:
        category = "licensing"
    elif "4022" in filename:
        category = "certification"
    elif "qa" in filename or "qapi" in filename:
        category = "qa"
    else:
        category = "misc"

    category_dir = UPLOAD_DIR / category
    os.makedirs(category_dir, exist_ok=True)

    file_path = category_dir / file.filename
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    return {
        "filename": file.filename,
        "category": category,
        "saved_to": str(file_path),
        "message": f"File saved to {category_dir}"
    }

