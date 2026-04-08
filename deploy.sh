#!/bin/bash

# Configuration
PROJECT_ID="your-project-id"
REGION="us-central1"

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

echo "Deployment complete!"
