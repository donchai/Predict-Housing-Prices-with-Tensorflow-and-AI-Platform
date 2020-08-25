# Predict Housing Prices with Tensorflow and AI Platform - Google Cloud Qwiklabs

## Objective

Automate deployment, simplify provisioning steps to achieve speed and accuracy.

## Guide

### Steps to perform this Qwiklabs
1. Visit lab URL (https://google.qwiklabs.com/focuses/3644?parent=catalog) and login to your Qwiklabs account
2. Launch this lab
3. Open Google Console
4. Accept Google Cloud Platform Terms of Service
5. Activate Cloud Shell
6. Type following command and hit enter  
source <(curl -s https://raw.githubusercontent.com/donchai/Predict-Housing-Prices-with-Tensorflow-and-AI-Platform/master/predict.sh)
7. Follow on screen instruction on Cloud Shell to complete this lab

## Screenshot
1. Accept Google Cloud Platform Terms of Service  
![alt text](https://github.com/donchai/Predict-Housing-Prices-with-Tensorflow-and-AI-Platform/blob/master/screenshots/tnc.png?raw=true) 
2. Stage 1 "Create Storage Bucket"  
![alt text](https://github.com/donchai/Predict-Housing-Prices-with-Tensorflow-and-AI-Platform/blob/master/screenshots/step1.png?raw=true) 
3. Stage 2 "Create the AI Platform notebook instance"
![alt text](https://github.com/donchai/Predict-Housing-Prices-with-Tensorflow-and-AI-Platform/blob/master/screenshots/step2.png?raw=true) 
4. Stage 3 "Download lab notebook"
![alt text](https://github.com/donchai/Predict-Housing-Prices-with-Tensorflow-and-AI-Platform/blob/master/screenshots/step3.png?raw=true) 
5. Stage 4 Before Complete "Train and deploy the Model for Predictions"
![alt text](https://github.com/donchai/Predict-Housing-Prices-with-Tensorflow-and-AI-Platform/blob/master/screenshots/step4-beforecomplete.png?raw=true) 
6. Stage 4 After Complete "Train and deploy the Model for Predictions"
![alt text](https://github.com/donchai/Predict-Housing-Prices-with-Tensorflow-and-AI-Platform/blob/master/screenshots/step4-aftercomplete.png?raw=true) 

## How It Works
Original training file "cloud-ml-housing-prices.ipynb" was simplified (removed markdown and extracted bash commands into bash shell script) and only left with Jupyter notebook executable syntax.  
A single bash script was created with extracted bash commands from original training file and were coded systematically to be executed as per lab requirement.

## Help
Contributors are welcome to participate in enhancing the automate deployment e.g.  
  -- Accepting Google Cloud Platform Terms of Service  
  -- Enhance the scripts to speed up the deployment time
  -- Others

## Credit
Senpai Gil - The Linux Guru for sharing command tip and trick.

## Limitation
Unable to accept Google Cloud Term and Condition from SDK/API, still exploring alternative to automate this manual step.

## Workaround
Login to Google Cloud Console and accept Google Cloud Platform Terms of Service.

## Reference 
https://google.qwiklabs.com/focuses/3644?parent=catalog
