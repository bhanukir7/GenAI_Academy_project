import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

# Configuration
project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "urcloudoptimizer")
api_key = os.environ.get("GEMINI_API_KEY")

class AnalysisRequest(BaseModel):
    text: str

class AnalysisResponse(BaseModel):
    classification: str

@app.get("/api/health")
async def health_check():
    return {
        "status": "ok",
        "project_id": project_id,
        "api_key_configured": api_key is not None,
        "mode": "Gemini API (Backend)"
    }

@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_sentiment(request: AnalysisRequest):
    if not api_key:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY is not configured on the server.")
    
    try:
        client = genai.Client(api_key=api_key)
        
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=f"Classify this financial news as 'Bullish', 'Bearish', or 'Neutral': {request.text}",
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=AnalysisResponse,
            ),
        )
        
        return response.parsed
    except Exception as e:
        print(f"Analysis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if os.path.exists("dist"):
    app.mount("/", StaticFiles(directory="dist", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))
