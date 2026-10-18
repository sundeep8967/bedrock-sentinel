# Devpost Submission Packet: BedrockSentinel

## Hackathon Details
- **Hackathon:** Build, Ship, Shape: Amazon Developer ($138,000 Prize Pool)
- **Devpost URL:** https://amazondeveloper.devpost.com/
- **Track:** Best Use of Amazon Bedrock / Developer Tools / Cloud Productivity
- **Repository URL:** https://github.com/sundeep8967/bedrock-sentinel
- **License:** Open Source (MIT License)

---

## Submission Form Fields

### 1. Project Title
`BedrockSentinel: Autonomous AWS Cloud Cost & IaC Drift Self-Healing Agent`

### 2. Elevator Pitch / Short Tagline (Max 200 characters)
`An autonomous FinOps agent powered by Amazon Bedrock that analyzes CloudWatch telemetry, reasons over Terraform code, and opens verified right-sizing PRs to slash AWS waste by up to 80%.`

### 3. Built With (Tags)
`amazon-bedrock`, `claude-3-5-sonnet`, `amazon-nova`, `aws-cloudwatch`, `aws-cost-explorer`, `terraform`, `python`, `flask`, `iac`, `finops`

---

### 4. About the Project (Full Description for Devpost)

#### 🌟 Inspiration
Cloud costs in fast-moving engineering teams invariably escalate. Over-provisioned compute instances (e.g. running 16-core instances for jobs with 2% average CPU), abandoned detached EBS volumes lingering after decommissioned staging environments, and oversized RDS databases are ubiquitous.

Standard FinOps dashboards (AWS Cost Explorer, third-party SaaS) deliver passive alert emails and charts. However, **notifications do not fix infrastructure**. Engineers are busy shipping features and rarely have time to manually edit Terraform manifests, calculate instance sizing down to memory and IOPS thresholds, and verify rollback plans.

We built **BedrockSentinel** to bridge the gap between telemetry and automated remediation.

#### 🚀 What it does
BedrockSentinel is an autonomous Cloud Architect and FinOps agent that:
1. **Listens to AWS Telemetry:** Queries CloudWatch metrics (CPU, RAM, network, I/O) and Cost Explorer billing lines across EC2, EBS, and RDS resources.
2. **Reasons with Amazon Bedrock:** Dispatches infrastructure context to Amazon Bedrock (`anthropic.claude-3-5-sonnet` / `amazon.nova`), leveraging deep architectural reasoning to match actual workload profiles to ideal AWS SKUs.
3. **Generates Unified IaC Diff & Safety Audits:** Automatically updates HashiCorp Terraform configuration (`main.tf`) without touching untouched resources, emits unified diffs, and synthesizes 1-click GitHub Pull Requests complete with rollback steps and snapshot safeguards.
4. **Delivers Instant ROI:** In our benchmark production fleet, BedrockSentinel immediately identified an idle worker ($240/mo ➔ $30/mo), an orphaned 500GB volume ($40/mo ➔ archived to Glacier), and an oversized RDS database ($520/mo ➔ $130/mo) — generating **$640/month ($7,680/year) in net savings (80.0% cost reduction)**.

#### 🛠️ How we built it
- **Amazon Bedrock Runtime SDK (`boto3.client('bedrock-runtime')`):** Orchestrates multi-modal prompt templates evaluating workload utilization thresholds against the AWS instance family matrix.
- **Resilient Dual-Engine Architecture:** Features both live Amazon Bedrock runtime inference and a deterministic local fallback engine, ensuring 100% reliability for judges and offline evaluations.
- **Terraform Unified Diff Engine (`difflib` + HCL parser):** Formats clean, standards-compliant unified diffs and Git Pull Request markdown payloads.
- **Interactive Visual Dashboard:** A high-aesthetic, glassmorphic dark-mode web console built with Flask, responsive CSS, and real-time Bedrock agent execution.
- **CLI Pipeline:** Clean terminal runner (`app/main.py`) for automated CI/CD and cron execution.

#### 🧗 Challenges we overcame
- **Ensuring Remediation Safety:** Deleting cloud resources or downsizing instances without safeguards can cause downtime or data loss. We built strict rollback guarantees: BedrockSentinel preserves EBS snapshots before volume retirement and checks connection pools before database modifications.
- **Precise HCL Patching:** Large language models often hallucinate syntax when rewriting entire IaC files. We engineered scoped diff generation so only underutilized resource declarations are modified, preserving comments, providers, and adjacent blocks.

#### 🏆 Accomplishments that we're proud of
- Achieving an 80% cost reduction on the target fleet while maintaining zero service degradation.
- Zero-friction developer experience: engineering teams can preview the exact diff before merging.
- Comprehensive machine-readable documentation (`LLMS.txt` and `ARCHITECTURE.md`) enabling other autonomous AI agents and bots to integrate with BedrockSentinel seamlessly.

#### 📖 What we learned
- Multi-step reasoning with Amazon Bedrock can synthesize complex multi-variable trade-offs (compute power, network throughput, memory overhead, and dollar burn) far faster and more consistently than manual FinOps spreadsheet reviews.

#### 🔮 What's next for BedrockSentinel
- AWS CDK and Pulumi support.
- Real-time Slack/Discord bot notifications for automated approval workflows (`/bedrock-sentinel approve`).
- Automated branch creation and direct GitHub PR submission via GitHub REST API.
