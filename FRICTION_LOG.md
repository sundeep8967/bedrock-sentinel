# Amazon Bedrock & AWS Developer Friction Log

- **Project:** BedrockSentinel
- **Repository:** https://github.com/sundeep8967/bedrock-sentinel

---

### Task Attempted
Implementing cross-region Amazon Bedrock model invocation (Claude 3.5 Sonnet / Amazon Nova) and scoped IAM permission policies for an autonomous remediation agent.

### Steps Taken
1. Configured the boto3 Bedrock client in Python with standard AWS IAM credentials.
2. Targeted `us-east-1` and `us-west-2` model endpoints for reasoning over CloudWatch metrics and HCL diff generation.
3. Attempted to scope down IAM actions to `bedrock:InvokeModel` and `bedrock:InvokeModelWithResponseStream` under a least-privilege role.

### Expected Result
Smooth model invocation with intuitive error handling and clearly documented IAM resource ARNs for Bedrock models across regions.

### Actual Result
Encountered cryptic `AccessDeniedException` errors when invoking certain foundation model IDs across regions, requiring manual cross-referencing between AWS Model Availability tables and IAM ARN wildcards. Regional quota and throughput limits for real-time streaming also lacked unified telemetry in the standard boto3 response.

### Severity Rating
Medium (P2) - slow down during agent onboarding and initial deployment.

### Workaround Used
Implemented a regional fallback and health-check retry wrapper around the Bedrock boto3 client, and created a consolidated, tested IAM policy document directly inside the project repository.

### Actionable Suggestion
1. Provide pre-packaged AWS CloudFormation / Terraform IAM templates with ready-to-use least-privilege roles specifically tailored for autonomous Bedrock agents.
2. Enhance Bedrock boto3 error exceptions to include the specific missing IAM action and regional availability status in the error body.
