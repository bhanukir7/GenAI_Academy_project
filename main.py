import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from google import genai
from google.genai import types

app = FastAPI()

# Initialize Vertex AI Client
# When vertexai=True, it uses the service account's credentials (ADC)
# and does not require an API key.
client = genai.Client(
    vertexai=True, 
    project=os.environ.get("GOOGLE_CLOUD_PROJECT"), 
    location=os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
)

class NewsInput(BaseModel):
    input: str

@app.post("/chat")
@app.post("/invoke")
async def classify_news(data: NewsInput):
    if not data.input:
        raise HTTPException(status_code=400, detail="Input text is required")

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
            model="gemini-1.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )

        return response.parsed

    except Exception as e:
        print(f"Error during classification: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Serve static files from the 'dist' directory
if os.path.exists("dist"):
    app.mount("/", StaticFiles(directory="dist", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    # Port 3000 is the only externally accessible port
    port = int(os.environ.get("PORT", 3000))
    uvicorn.run(app, host="0.0.0.0", port=port)
