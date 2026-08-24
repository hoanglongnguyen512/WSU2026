# COMP2029 - DevOps Project

**Student:** Hoang Long Nguyen  
**Student ID:** 22121402  

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
Extended the previous monitoring function into a full **Web Health Crawler** system. The system periodically checks multiple websites, collects availability and latency metrics, and visualizes the data using CloudWatch.

### Features
- Web Crawler that monitors multiple websites
- Collects **Availability** and **Latency** metrics
- Publishes custom metrics to **Amazon CloudWatch** using Boto3
- Automatically runs every **30 minutes** using EventBridge
- CloudWatch **Alarms** for high latency and low availability
- CloudWatch **Dashboard** for real-time visualization
- Infrastructure as Code using **AWS CDK** (Python)

### Monitored Websites
- https://www.westernsydney.edu.au/
- https://www.google.com/
- https://www.github.com/
- https://aws.amazon.com/

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


How to Test

Go to AWS Lambda Console → select WebHealthCrawler
Click Test
View results (availability + latency for each website)
Go to CloudWatch → Dashboards → WebHealth-Dashboard

DevOps Principles Applied

Automation: Fully automated monitoring and metric collection
Monitoring & Feedback: Real-time metrics and alarms
Infrastructure as Code: Entire infrastructure defined in CDK
Continuous Improvement: Regular scheduled health checks


Author
Hoang Long Nguyen 
Student ID : 22121402

Western Sydney University – Bachelor of ICT