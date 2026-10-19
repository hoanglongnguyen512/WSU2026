# COMP2029 - DevOps Project

**Student:** Hoang Long Nguyen  
**Student ID:** 22121402  
**University:** Western Sydney University – Bachelor of ICT

---

## Project Overview
This project implements a serverless web health monitoring system using AWS CDK. The system periodically checks the availability and latency of multiple websites, publishes metrics to CloudWatch, triggers alarms, and supports dynamic website management through a public REST API.

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

---

## Week 03 - Building the Foundation of DevOps

### Description
Extended the system into a multi-website health crawler with CloudWatch integration.

### Features
- Monitors multiple websites
- Collects **Availability** and **Latency** metrics
- Publishes custom metrics to **Amazon CloudWatch** using Boto3
- Runs every **30 minutes** using EventBridge
- CloudWatch **Alarms** for high latency and low availability
- CloudWatch **Dashboard** for real-time visualization
- Infrastructure as Code using **AWS CDK** (Python)

---

## Week 04 - Building the Foundation of DevOps (Continued)

### Description
Continued refining monitoring practices and infrastructure setup.

---

## Week 05 - The First Way (Flow)

### Description
Focused on improving the flow of the monitoring pipeline and automation.

---

## Week 06 - The First Way (Continued)

### Description
Added SNS notifications for CloudWatch alarms and began logging alarm events.

### Features
- SNS topic for alarm notifications
- Email subscription for alerts

---

## Week 07 - The Second Way (Feedback)

### Description
Implemented alarm logging into DynamoDB for historical tracking.

### Features
- DynamoDB table (`WebHealthAlarmTable`) to store alarm events
- Lambda function (`AlarmLogger`) to process SNS messages and write to DynamoDB

---

## Week 09 - The Third Way (Continual Learning & Experimentation)

### Description
Focused on testing practices and continuous improvement of the monitoring system.

---

## Week 10 - Testing

### Description
Integrated unit, functional, and integration tests into the project.

### Tests Implemented
- **10** Unit Tests
- **8** Functional Tests
- **2** Integration Tests

---

## Week 11 - Continual Learning

### Description
Further refinement of the system and documentation.

---

## Applied Project - Dynamic Website Management

### Overview : 
Extended the system to support dynamic website management using DynamoDB and a public REST API. Websites are no longer hardcoded.

### Features : 
- Websites are stored in a **DynamoDB table** (`WebsiteTable`)
- Public **REST API** (API Gateway + Lambda) for managing websites
- Crawler reads the website list from DynamoDB on every run
- Full Infrastructure as Code with AWS CDK

### Monitored Websites
The following websites are currently being monitored (managed via DynamoDB):
- https://www.google.com
- https://www.westernsydney.edu.au
- https://www.github.com
- https://aws.amazon.com

### API Endpoints
- `GET /websites` — List all monitored websites
- `POST /websites` — Add a new website

## API Documentation

Base URL: `https://8fx0uzj22b.execute-api.ap-southeast-2.amazonaws.com/prod`

### GET /websites
List all monitored websites.

**Response:**
```json
[{"url": "https://www.google.com"}]
POST /websites
Add a new website to monitor.
Request:S
JSON{"url": "https://example.com"}
Response:
JSON{"message": "Website added", "url": "https://example.com"}
DELETE /websites/{url}
Remove a website from monitoring.
Example:
textDELETE /websites/https://example.com
Response:
JSON{"message": "Website deleted"}

### API BASE URL
https://8fx0uzj22b.execute-api.ap-southeast-2.amazonaws.com/prod/

### How to Test the API
```powershell
# Add a website
Invoke-RestMethod -Method Post -Uri "https://8fx0uzj22b.execute-api.ap-southeast-2.amazonaws.com/prod/websites" -ContentType "application/json" -Body '{"url":"https://www.github.com"}'

# List websites
Invoke-RestMethod -Method Get -Uri "https://8fx0uzj22b.execute-api.ap-southeast-2.amazonaws.com/prod/websites"
```


### Running Tests
This project includes unit, functional, and integration tests for the web crawler.

### Install test dependencies
```bash
pip install pytest boto3
```

## Run all tests
```bash
pytest -v
```

## Run specific test files

# Unit tests
```bash
pytest tests/test_unit.py -v 
```

# Functional tests 
```bash
pytest tests/test_functional.py -v
```

# Integration tests
```bash
pytest tests/test_integration.py -v
```

### Test Summary
- 10 unit tests 
- 8 functional tests 
- 2 integration tests

---

### Architecture : 
- **Compute:** AWS Lambda (Python 3.12)
- **Scheduling:** Amazon EventBridge
- **Monitoring:** Amazon CloudWatch (Metrics, Alarms, Dashboard)
- **Notifications:** Amazon SNS
- **Storage:** Amazon DynamoDB
- **API:** Amazon API Gateway
- **IaC:** AWS CDK
- **Region:** ap-southeast-2 (Sydney)

---

### DevOps Principles Applied :

- Automation: Scheduled monitoring and metric collection
- Monitoring & Feedback: CloudWatch metrics, alarms, and SNS notifications
- Infrastructure as Code: Entire infrastructure defined in CDK
- Continuous Improvement: Dynamic website management and comprehensive testing

---

**Author**

Hoang Long Nguyen
Student ID: 22121402
Western Sydney University – Bachelor of ICT