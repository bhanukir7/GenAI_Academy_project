#!/bin/bash

# Configuration
PROJECT_ID="your-project-id"
REGION="us-central1"

# 1. Build Frontend
echo "Building frontend..."
npm run build

# 2. Initialize Terraform
echo "Initializing Terraform..."
cd terraform
terraform init

# 3. Create Artifact Registry (if it doesn't exist)
# We apply just the repo first so we can push to it
terraform apply -target=google_artifact_registry_repository.repo -var="project_id=$PROJECT_ID" -var="region=$REGION" -auto-approve

# 4. Build and Push Docker Image
REPO_URL="$REGION-docker.pkg.dev/$PROJECT_ID/financial-news-classifier/app:latest"
echo "Building and pushing Docker image to $REPO_URL..."
cd ..
gcloud auth configure-docker $REGION-docker.pkg.dev
docker build -t $REPO_URL .
docker push $REPO_URL

# 5. Deploy with Terraform
echo "Deploying to Cloud Run..."
cd terraform
terraform apply -var="project_id=$PROJECT_ID" -var="region=$REGION" -auto-approve

echo "Deployment complete!"
