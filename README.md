# Financial News Sentiment Classifier

A production-ready, full-stack application that classifies financial news snippets into **Bullish**, **Bearish**, or **Neutral** categories using Google's Gemini 3 Flash model via Vertex AI.

## 🚀 Features

- **Real-time Classification:** Instant sentiment analysis of financial headlines.
- **Enterprise Security:** Uses **Keyless IAM-based authentication** with Vertex AI. No API keys are stored or exposed.
- **Production-Grade Backend:** FastAPI server handles AI logic and serves the frontend.
- **Modern Frontend:** React + Tailwind CSS + Lucide Icons for a polished UI.
- **Infrastructure as Code:** Fully automated deployment using Terraform.
- **Containerized:** Dockerized for consistent deployment on Google Cloud Run.

## 🛠️ Tech Stack

- **Frontend:** React, TypeScript, Tailwind CSS, Lucide React, Framer Motion.
- **Backend:** Python, FastAPI, Vertex AI SDK (`google-genai`).
- **Infrastructure:** Terraform, Google Cloud Run, Artifact Registry.
- **AI Model:** Gemini 3 Flash (via Vertex AI).

## 🏗️ Architecture

This project follows Google Cloud best practices for security:
1. **Frontend** sends news snippets to the **Backend**.
2. **Backend** (running on Cloud Run) uses its **Service Account identity** to call **Vertex AI**.
3. **IAM Permissions** (`roles/aiplatform.user`) are granted to the service account via Terraform.
4. **Vertex AI** processes the request and returns a structured JSON response.

## 📋 Prerequisites

- [Google Cloud Project](https://console.cloud.google.com/) with billing enabled.
- **Enable Vertex AI API:** Go to the [Vertex AI API](https://console.cloud.google.com/apis/library/aiplatform.googleapis.com) page and click **Enable**.
- [Google Cloud CLI](https://cloud.google.com/sdk/docs/install) installed and authenticated.
- [Docker](https://www.docker.com/) installed.
  - **WSL 2 Users:** Ensure Docker Desktop is running and "WSL Integration" is enabled for your specific distro in Docker Desktop settings.
- [Terraform](https://www.terraform.io/) installed.
- [Node.js](https://nodejs.org/) and [Python 3.10+](https://www.python.org/) for local development.

## 🚀 Deployment

1. **Configure Project ID:**
   Open `deploy.sh` and update the `PROJECT_ID` variable:
   ```bash
   PROJECT_ID="your-google-cloud-project-id"
   ```

2. **Run Deployment Script:**
   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```

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
