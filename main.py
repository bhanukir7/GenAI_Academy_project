import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

app = FastAPI()

# Initialize Vertex AI Client
project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
api_key = os.environ.get("GEMINI_API_KEY")

if not project_id:
    print("WARNING: GOOGLE_CLOUD_PROJECT environment variable is not set.")

# Use Vertex AI if project_id is present, otherwise fallback to Gemini API if key is present
if project_id:
    print(f"Initializing GenAI Client with Vertex AI (Project: {project_id}, Location: {location})")
    client = genai.Client(
        vertexai=True, 
        project=project_id, 
        location=location
    )
elif api_key:
    print("Initializing GenAI Client with Gemini API Key (Fallback)")
    client = genai.Client(api_key=api_key)
else:
    print("WARNING: Neither GOOGLE_CLOUD_PROJECT nor GEMINI_API_KEY is set. AI calls will fail.")
    # We still initialize to avoid NameError, but it will fail on use
    client = None

class NewsInput(BaseModel):
    input: str

@app.get("/api/health")
async def health_check():
    return {
        "status": "ok",
        "project_id": project_id,
        "location": location,
        "has_api_key": bool(api_key),
        "mode": "Vertex AI" if project_id else "Gemini API" if api_key else "None",
        "model": "gemini-3-flash-preview"
    }

@app.post("/chat")
@app.post("/invoke")
async def classify_news(data: NewsInput):
    if not data.input:
        raise HTTPException(status_code=400, detail="Input text is required")

    if not client:
        raise HTTPException(
            status_code=500, 
            detail="AI Client not initialized. Please set GOOGLE_CLOUD_PROJECT or GEMINI_API_KEY."
        )

    try:
        prompt = f"""
        Act as a Senior Financial Analyst. 
        Classify the following financial news snippet into one of these categories: 'Bullish', 'Bearish', or 'Neutral'.
        
        Rules:
        - Return ONLY a JSON object.
        - The JSON object must have a single key "classification" with the value being one of the three categories.
        
        News Snippet: "{data.input}"
        """

        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )

        if not response.parsed:
            # Fallback if parsing fails or returns null
            return {"classification": "Neutral"}

        return response.parsed

    except Exception as e:
        error_msg = str(e)
        print(f"Error during classification: {error_msg}")
        # Return a structured error that the frontend can parse
        raise HTTPException(
            status_code=500, 
            detail={
                "message": "AI Analysis failed",
                "error": error_msg,
                "suggestion": "If running locally/preview, ensure GOOGLE_CLOUD_PROJECT is set or GEMINI_API_KEY is available. If deployed, check IAM permissions."
            }
        )

# Serve static files from the 'dist' directory
if os.path.exists("dist"):
    app.mount("/", StaticFiles(directory="dist", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    # Port 3000 is the only externally accessible port
    port = int(os.environ.get("PORT", 3000))
    uvicorn.run(app, host="0.0.0.0", port=port)
