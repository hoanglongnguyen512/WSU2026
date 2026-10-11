# COMP2029 - DevOps Project

**Student:** Hoang Long Nguyen  
**Student ID:** 22121402  
**University:** Western Sydney University – Bachelor of ICT

---

## Week 02 - The Three Ways

### Project Description
This project uses **AWS CDK** to deploy a serverless Lambda function that monitors the availability and performance of a web resource.

### Features
- Measures HTTP status code
- Measures response time (milliseconds)
- Returns structured JSON result
- Deployed using Infrastructure as Code (AWS CDK)

### Target Website
- https://www.westernsydney.edu.au/

### Architecture
- Runtime: Python 3.12
- Infrastructure: AWS Lambda + AWS CDK
- Region: ap-southeast-2 (Sydney)

---

## Week 03 - Building the Foundation of DevOps

### Project Overview
Extended the monitoring function into a full **Web Health Crawler** system. The system periodically checks multiple websites, collects availability and latency metrics, and visualizes the data using CloudWatch.

### Features
- Monitors multiple websites
- Collects **Availability** and **Latency** metrics
- Publishes custom metrics to **Amazon CloudWatch** using Boto3
- Runs every **30 minutes** using EventBridge
- CloudWatch **Alarms** for high latency and low availability
- CloudWatch **Dashboard** for real-time visualization
- Infrastructure as Code using **AWS CDK** (Python)

### Architecture
- **Compute:** AWS Lambda (Python 3.12)
- **Scheduling:** Amazon EventBridge
- **Monitoring:** Amazon CloudWatch (Metrics + Alarms + Dashboard)
- **IaC:** AWS CDK
- **Region:** ap-southeast-2 (Sydney)

### How to Deploy
```bash
source .venv/bin/activate
cdk deploy

### How to Test
1. Go to **AWS Lambda Console** → select `WebHealthCrawler`
2. Click **Test**
3. View results (availability + latency for each website)
4. Go to **CloudWatch → Dashboards → WebHealth-Dashboard**
 
 ---

## Applied Project - Dynamic Website Management

### Overview : 
The system has been extended to support dynamic website management using DynamoDB and a public REST API. Websites are no longer hardcoded.

### Features : 
- Websites are stored in a **DynamoDB table** (`WebsiteTable`)
- Public **REST API** (API Gateway + Lambda) for managing websites
- Crawler reads the website list from DynamoDB on every run
- Full Infrastructure as Code with AWS CDK

### API URL
https://8fx0uzj22b.execute-api.ap-southeast-2.amazonaws.com/prod/

### How to Test the API
```powershell
# Add a website
Invoke-RestMethod -Method Post -Uri "https://8fx0uzj22b.execute-api.ap-southeast-2.amazonaws.com/prod/websites" -ContentType "application/json" -Body '{"url":"https://www.github.com"}'

# List websites
Invoke-RestMethod -Method Get -Uri "https://8fx0uzj22b.execute-api.ap-southeast-2.amazonaws.com/prod/websites"

### Architecture : 
- DynamoDB: WebsiteTable (stores website URLs)
- Lambda: WebsiteApi (CRUD handler)
- API Gateway: Public REST API
- Crawler: Reads websites from DynamoDB


### DevOps Principles Applied :

- Automation: Fully automated monitoring and metric collection
- Monitoring & Feedback: Real-time metrics, alarms, and dashboard
- Infrastructure as Code: Entire infrastructure defined in CDK
- Continuous Improvement: Dynamic website management via API

---

**Author**

Hoang Long Nguyen
Student ID: 22121402
Western Sydney University – Bachelor of ICT