
# AI Assistant

This repository contains a Python-based AI assistant built using AWS Bedrock. The assistant is designed to automate the creation of AWS Lambda functions based on user inputs, can perform various mathematical calculations, and send an email.

## Prerequisites

- Python 3.12 or higher
- AWS account with appropriate permissions for Lambda and S3
- AWS CLI configured with your credentials

## Setup

### 1. Install Dependencies

Before you begin, ensure all the required packages are installed by running:

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Make sure to set up the required environment variables before running the agent. These variables are crucial for connecting to your AWS resources.

```bash
export LAMBDA_ROLE=REPLACE_WITH_LambdaRole
export S3_BUCKET=REPLACE_WITH_DataAnalysisS3Bucket
```

Replace `REPLACE_WITH_LambdaRole` with your actual Lambda role ARN and `REPLACE_WITH_DataAnalysisS3Bucket` with the name of your S3 bucket used for data analysis.

### 3. Running the Agent

To run the agent, execute:

```bash
python agent.py
```

This will start the AI agent and allow it to interact with AWS services as configured.

## Usage

The agent is designed to:

- Collect user inputs for function name, runtime, handler, and other configurations.
- Automatically create and deploy AWS Lambda functions using the provided inputs.
- Perform various mathematical calculations as requested by the user.
- Store related function data in the specified S3 bucket for reference.
- Send an email using a lambda function

Make sure that your AWS Lambda function and S3 bucket are properly configured to match the environment variables.

## Architecture

```mermaid
graph TD;
    UserInput -->|Triggers| AI_Assistant
    AI_Assistant -->|Creates| Lambda_Function
    AI_Assistant -->|Sends| Email
    Lambda_Function -->|Stores Data| S3_Bucket
    AI_Assistant -->|Performs| Calculations
```
```mermaid
flowchart TD
    Agent["AI Agent using Bedrock and Claude 3 Haiku"]
    Claude3Haiku["Claude 3 Haiku Model"]
    DecisionPoint{"Decision Point"}

    Agent -->|Uses| Claude3Haiku
    Claude3Haiku -->|Processes User Message| DecisionPoint

    sendEmail["Send Email Tool"]
    cosine["Cosine Tool"]
    lambdaGen["Lambda Function Generator"]

    DecisionPoint -->|Email related message| sendEmail
    DecisionPoint -->|Similarity Calculation| cosine
    DecisionPoint -->|Lambda Function request| lambdaGen
    DecisionPoint -->|Returns| llmResponse["LLM Response Processor"]

    toolsFile["tools.py"]
    awsClientsFile["aws_clients.py"]
    llmUtilsFile["llm_utils.py"]
    llmResponseProcessorFile["llm_response_processor.py"]
    lambdaUtilsFile["lambda_utils.py"]
    agentFile["agent.py"]

    Agent -->|Executes| agentFile
    agentFile --> toolsFile
    agentFile --> awsClientsFile
    agentFile --> llmUtilsFile
    agentFile --> llmResponseProcessorFile
    agentFile --> lambdaUtilsFile
    llmUtilsFile -->|Makes request to| Claude3Haiku
    llmResponseProcessorFile -->|Generates| llmResponse
    lambdaGen -->|Uses| lambdaUtilsFile

    sendEmail --> toolsFile
    cosine --> toolsFile
    lambdaGen --> toolsFile
```
```mermaid
graph TD
    classDef fileStyle shape:rect,fill:#f3f3f3,stroke:#333,stroke-width:2px,rx:5px,ry:5px;
    classDef folderStyle shape:rect,fill:#dcdcdc,stroke:#333,stroke-width:2px,rx:5px,ry:5px;

    root["/project-root"]:::folderStyle
    root --> src["/src"]:::folderStyle
    src --> agentFile["agent.py"]:::fileStyle@{ shape: doc }
    src --> toolsFile["tools.py"]:::fileStyle@{ shape: doc }
    src --> awsClientsFile["aws_clients.py"]:::fileStyle@{ shape: doc }
    src --> llmUtilsFile["llm_utils.py"]:::fileStyle@{ shape: doc }
    src --> llmResponseProcessorFile["llm_response_processor.py"]:::fileStyle@{ shape: doc }
    src --> lambdaUtilsFile["lambda_utils.py"]:::fileStyle@{ shape: doc }

    agentFile --> toolsFile
    agentFile --> awsClientsFile
    agentFile --> llmUtilsFile
    agentFile --> llmResponseProcessorFile
    agentFile --> lambdaUtilsFile
    toolsFile --> sendEmailTool(("Send Email Tool"))
    toolsFile --> cosineTool(("Cosine Tool"))
    toolsFile --> lambdaGenTool(("Lambda Function Generator"))
    llmUtilsFile --> Claude3Haiku["Claude 3 Haiku Model"]

    class agentFile,toolsFile,awsClientsFile,llmUtilsFile,llmResponseProcessorFile,lambdaUtilsFile fileStyle;
    class root,src folderStyle;

```

## License

AWS Amazon
