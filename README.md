# Financial News Sentiment Classifier

A production-ready, full-stack application that classifies financial news snippets into **Bullish**, **Bearish**, or **Neutral** categories using Google's **Gemini 3 Flash** model via the direct Gemini API.

## 🚀 Features

- **Real-time Classification:** Instant sentiment analysis of financial headlines.
- **Gemini API Integration:** Uses the direct Gemini API for fast and reliable analysis.
- **Production-Grade Backend:** FastAPI server serves the React frontend.
- **Modern Frontend:** React + Tailwind CSS + Lucide Icons for a polished UI.
- **Infrastructure as Code:** Fully automated deployment using Terraform.
- **Containerized:** Dockerized for consistent deployment on Google Cloud Run.

## 🛠️ Tech Stack

- **Frontend:** React, TypeScript, Tailwind CSS, Lucide React, Framer Motion, `@google/genai`.
- **Backend:** Python, FastAPI.
- **Infrastructure:** Terraform, Google Cloud Run, Artifact Registry.
- **AI Model:** Gemini 3 Flash.

## 🏗️ Architecture

1. **Frontend** calls the **Gemini API** directly using the `@google/genai` SDK.
2. **Backend** (running on Cloud Run) serves the static frontend files and provides a health check endpoint.
3. **Deployment** is automated via a shell script and Terraform.

## 📋 Prerequisites

- [Google Cloud Project](https://console.cloud.google.com/) with billing enabled.
- **Gemini API Key:** Obtain an API key from [Google AI Studio](https://aistudio.google.com/).
- [Google Cloud CLI](https://cloud.google.com/sdk/docs/install) installed and authenticated.
- [Docker](https://www.docker.com/) installed.
- [Terraform](https://www.terraform.io/) installed.
- [Node.js](https://nodejs.org/) and [Python 3.10+](https://www.python.org/) for local development.

## 🚀 Deployment

1. **Configure Project ID:**
   Open `deploy.sh` and update the `PROJECT_ID` variable.

2. **Run Deployment Script:**
   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```

3. **Set API Key:**
   After deployment, ensure the `GEMINI_API_KEY` environment variable is set in your Cloud Run service.

### 🛠️ Troubleshooting Common Errors

- **`vite: Permission denied`**: The script now automatically runs `npm install` and fixes permissions. If it persists, try running `chmod +x node_modules/.bin/vite` manually.
- **`docker: command not found`**: In WSL 2, this means Docker Desktop is either not running or the WSL integration is disabled. Check your Docker Desktop settings.
- **`Invalid quoted type constraints`**: This was a Terraform version compatibility issue which has been fixed in the provided `.tf` files.
   This script will:
   - Build the React frontend.
   - Initialize Terraform.
   - Create a Docker repository in Artifact Registry.
   - Build and push the Docker image.
   - Deploy the service to Cloud Run with correct IAM permissions.

## 💻 Local Development

### Backend
```bash
pip install -r requirements.txt
python main.py
```

### Frontend
```bash
npm install
npm run dev
```

## 💰 Cost Estimation (3 Days / 10 Queries)

| Component | Estimated Cost |
| :--- | :--- |
| **Cloud Run** | $0.00 (Free Tier) |
| **Vertex AI** | < $0.0001 |
| **Artifact Registry** | ~$0.01 |
| **Total** | **~$0.01** |

## 📄 License

MIT
