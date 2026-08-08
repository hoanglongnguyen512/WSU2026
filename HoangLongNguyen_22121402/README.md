
# Welcome to your CDK Python project!
#COMP2029 - DevOps Project

**Student:** Hoang Long Nguyen  
**Student ID:** 22121402  
**Week:** 02 - The Three Ways

## Project Description

This project uses **AWS CDK** to deploy a serverless Lambda function that monitors the availability and performance of a web resource.

### Features
- Measures HTTP status code
- Measures response time (milliseconds)
- Returns structured JSON result
- Deployed using Infrastructure as Code (AWS CDK)

### Target Website
- https://www.westernsydney.edu.au/

## Architecture
- Runtime: Python 3.12
- Infrastructure: AWS Lambda + AWS CDK
- Region: ap-southeast-2 (Sydney)

## How to Deploy
```bash
cdk deploy

This is a blank project for CDK development with Python.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `requirements.txt` file and rerun the `python -m pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
