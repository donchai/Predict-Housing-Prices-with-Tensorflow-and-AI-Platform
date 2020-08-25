#!/bin/bash

# Assign Programmatic Variables
export PROJECTID=$(gcloud config get-value project)
export ZONE="us-west1-b"
export REGION="us-central1"
export GCS_BUCKET="gs://$PROJECTID"

# Configure Cloud Shell Environment Variables
gcloud config set project $PROJECTID
gcloud config set compute/region $REGION

# Create Storage Bucket
gsutil mb gs://${PROJECTID}

# Check my progress
read -n1 -r -p "Click \"#1 Create Storage Bucket\" [Check my progress] button to complete, once done press any key to continue to next stage 2/4..." 

# Enable Notebooks API
gcloud services enable notebooks.googleapis.com

# Create Notebooks Instance in zone us-west1-b
gcloud beta notebooks instances create $PROJECTID \
  --vm-image-project=deeplearning-platform-release \
  --vm-image-family="tf-1-15-cpu" \
  --machine-type="n1-standard-4" \
  --location=${ZONE} \
  --quiet

# Check my progress
read -n1 -r -p "Click \"#2 Create the AI Platform notebook instance\" [Check my progress] button to complete, once done press any key to continue to next stage 3/4..."

# Download pre-simplified Jupyter Notebook from GitHub into temporary folder
curl -o /tmp/cloud-ml-housing-prices.ipynb https://raw.githubusercontent.com/donchai/Predict-Housing-Prices-with-Tensorflow-and-AI-Platform/master/training-data-analyst/blogs/housing_prices/cloud-ml-housing-prices.ipynb

# Remote into Notebooks Instance, Download and Prepare Training Script (simplified) from Github
gcloud compute ssh --project ${PROJECTID} --zone ${ZONE} ${PROJECTID} -- -v 'cd /home/jupyter && /usr/bin/sudo git clone https://github.com/GoogleCloudPlatform/training-data-analyst && /usr/bin/sudo curl -o /home/jupyter/Predict-Housing-Prices-with-Tensorflow-and-AI-Platform/master/training-data-analyst/blogs/housing_prices/cloud-ml-housing-prices.ipynb https://raw.githubusercontent.com/donchai/Predict-Housing-Prices-with-Tensorflow-and-AI-Platform/master/training-data-analyst/blogs/housing_prices/cloud-ml-housing-prices.ipynb && /usr/bin/sudo mkdir /home/jupyter/training-data-analyst/blogs/housing_prices/trainer && /usr/bin/sudo touch /home/jupyter/training-data-analyst/blogs/housing_prices/trainer/__init__.py && /usr/bin/sudo chown jupyter:jupyter -R /home/jupyter/training-data-analyst'

read -n1 -r -p "Click \"#3 Download lab notebook\" [Check my progress] button to complete, once done press any key to continue to next stage 4/4..."

# Remote into Notebooks Instance, Execute Jupyter Notebook
gcloud compute ssh --project ${PROJECTID} --zone ${ZONE} ${PROJECTID} -- -v 'cd /home/jupyter/training-data-analyst/blogs/housing_prices && /usr/bin/sudo /opt/conda/bin/jupyter nbconvert ml-housing-prices.ipynb --to notebook --clear-output --execute'

# Execute Google Cloud SDK for AI Platform
gcloud ai-platform local train \
  --module-name=trainer.task \
  --package-path=trainer \
  -- \
  --output_dir='./output'

export REGION="us-central1"
export GCS_BUCKET="gs://$PROJECTID"

export JOBNAME="housing_$(date -u +%y%m%d_%H%M%S)"

gcloud ai-platform jobs submit training $JOBNAME \
  --region=$REGION \
  --module-name=trainer.task \
  --package-path=./trainer \
  --job-dir=$GCS_BUCKET/$JOBNAME/ \
  --runtime-version 1.15 \
  -- \
  --output_dir=$GCS_BUCKET/$JOBNAME/output

export JOBNAME="housing_$(date -u +%y%m%d_%H%M%S)"

gcloud ai-platform jobs submit training $JOBNAME \
  --region=$REGION \
  --module-name=trainer.task \
  --package-path=./trainer \
  --job-dir=$GCS_BUCKET/$JOBNAME \
  --runtime-version 1.15 \
  --scale-tier=STANDARD_1 \
  -- \
  --output_dir=$GCS_BUCKET/$JOBNAME/output

export JOBNAME="housing_$(date -u +%y%m%d_%H%M%S)"

gcloud ai-platform jobs submit training $JOBNAME \
  --region=$REGION \
  --module-name=trainer.task \
  --package-path=./trainer \
  --job-dir=$GCS_BUCKET/$JOBNAME \
  --runtime-version 1.15 \
  --scale-tier=BASIC_GPU \
  -- \
  --output_dir=$GCS_BUCKET/$JOBNAME/output

export JOBNAME="housing_$(date -u +%y%m%d_%H%M%S)"

gcloud ai-platform jobs submit training $JOBNAME \
  --region=$REGION \
  --module-name=trainer.task \
  --package-path=./trainer \
  --job-dir=$GCS_BUCKET/$JOBNAME \
  --runtime-version 1.15 \
  --config config.yaml \
  -- \
  --output_dir=$GCS_BUCKET/$JOBNAME/output

export MODEL_NAME="housing_prices"
export MODEL_VERSION="v1"
export MODEL_LOCATION="output/export/Servo/$(ls output/export/Servo | tail -1)"

gcloud ai-platform versions delete ${MODEL_VERSION} --model ${MODEL_NAME}
gcloud ai-platform models delete ${MODEL_NAME}
gcloud ai-platform models create ${MODEL_NAME} --regions $REGION
gcloud ai-platform versions create ${MODEL_VERSION} --model ${MODEL_NAME} --origin ${MODEL_LOCATION} --staging-bucket=$GCS_BUCKET --runtime-version=1.15

gcloud ai-platform predict --model housing_prices --json-instances records.json

read -n1 -r -p "Click \"#4 Train and deploy the Model for Predictions\" [Check my progress] button to complete, once done press any key to complete."

