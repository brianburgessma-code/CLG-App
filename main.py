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
    summary = {"files_found": [], "report_summary": []}

    try:
        # Scan XM4 output folder
        for file in os.listdir(output_dir):
            if file.endswith(".json") or file.endswith(".csv"):
                summary["files_found"].append(file)

        # Example logic: look for the latest model report
        latest_json = sorted(
            [f for f in summary["files_found"] if f.startswith("XM4_Model_Report")],
            reverse=True
        )
        if latest_json:
            with open(os.path.join(output_dir, latest_json[0]), "r") as f:
                data = json.load(f)
            summary["report_summary"].append({
                "latest_report": latest_json[0],
                "keys": list(data.keys())[:5]  # preview
            })
        else:
            summary["report_summary"].append({"message": "No XM4 reports found."})

    except Exception as e:
        summary["error"] = str(e)

    return summary

