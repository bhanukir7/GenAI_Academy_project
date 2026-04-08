#!/bin/bash

# Configuration
PROJECT_ID="urcloudoptimizer"
REGION="us-central1" 
# Use a specific region for Vertex AI for better stability
AI_REGION="us-central1"

# 1. Check Dependencies
echo "Checking dependencies..."
for cmd in npm terraform gcloud docker; do
  if ! command -v $cmd &> /dev/null; then
    echo "Error: $cmd is not installed. Please install it before running this script."
    if [ "$cmd" = "docker" ]; then
      echo "Note: If you are using WSL 2, ensure Docker Desktop is running and WSL integration is enabled."
    fi
    exit 1
  fi
done

# 2. Build Frontend
echo "Installing dependencies and building frontend..."
npm install
chmod +x node_modules/.bin/vite
npm run build

# 3. Initialize Terraform
echo "Initializing Terraform..."
cd terraform
terraform init

# 4. Create Artifact Registry (if it doesn't exist)
echo "Creating Artifact Registry..."
terraform apply -target=google_artifact_registry_repository.repo -var="project_id=$PROJECT_ID" -var="region=$REGION" -auto-approve

# 5. Build and Push Docker Image
REPO_URL="$REGION-docker.pkg.dev/$PROJECT_ID/financial-news-classifier/app:latest"
echo "Building and pushing Docker image to $REPO_URL..."
cd ..
gcloud auth configure-docker $REGION-docker.pkg.dev --quiet
docker build -t $REPO_URL .
docker push $REPO_URL

# 6. Deploy with Terraform
echo "Deploying to Cloud Run..."
cd terraform
terraform apply -var="project_id=$PROJECT_ID" -var="region=$REGION" -auto-approve

# 7. ADD THIS STEP: Fix Environment Variables
# Terraform often doesn't set these by default. This ensures your main.py
# gets the correct Project ID and the 'global' location needed for Gemini 3.
echo "Configuring Service Environment Variables..."
gcloud run services update financial-news-classifier \
  --set-env-vars GOOGLE_CLOUD_PROJECT=$PROJECT_ID,GOOGLE_CLOUD_LOCATION=$AI_REGION \
  --region $REGION \
  --quiet

echo "Deployment complete! Your app is now using Project: $PROJECT_ID and Location: $AI_REGION"
