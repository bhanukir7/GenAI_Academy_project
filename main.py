import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

# Configuration
project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "urcloudoptimizer")
location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

@app.get("/api/health")
async def health_check():
    return {
        "status": "ok",
        "project_id": project_id,
        "location": location,
        "mode": "Gemini API (Frontend)"
    }

if os.path.exists("dist"):
    app.mount("/", StaticFiles(directory="dist", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))
