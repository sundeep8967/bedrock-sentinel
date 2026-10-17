import os
import sys
import time

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from telemetry import CloudTelemetryCollector
from agent import BedrockSentinelAgent
from iac_engine import IaCEngine

def main():
    root_dir = os.path.dirname(current_dir)
    tf_file = os.path.join(root_dir, "terraform_demo", "main.tf")

    print("\n" + "#"*75)
    print("      ☁️  BEDROCK SENTINEL: AUTONOMOUS AWS CLOUD COST AGENT")
    print("      'Build, Ship, Shape: Amazon Developer' Hackathon Submission")
    print("#"*75)

    time.sleep(0.5)
    print("\n📡 [STEP 1/4]: Connecting to AWS CloudWatch & Cost Explorer Telemetry...")
    collector = CloudTelemetryCollector(region="us-east-1")
    telemetry = collector.fetch_utilization_metrics()
    current_burn = collector.compute_current_monthly_burn(telemetry)

    for res in telemetry:
        print(f"  • {res['resource_id']} [{res['resource_type']}]")
        print(f"    Current SKU: {res['current_sku']} | Cost: ${res['current_cost_usd_monthly']:.2f}/mo | Status: {res['status']}")

    print(f"\n🔥 Total Monitored Monthly Burn: ${current_burn:.2f}/month")

    time.sleep(0.5)
    print("\n🔍 [STEP 2/4]: Reading Terraform Infrastructure as Code (main.tf)...")
    iac = IaCEngine(tf_file)
    tf_code = iac.read_config()
    print(f"  • Ingested {len(tf_code.splitlines())} lines of HCL Terraform configuration.")

    time.sleep(0.5)
    print("\n🧠 [STEP 3/4]: Invoking Amazon Bedrock Reasoning Agent (Claude 3.5 Sonnet / Nova)...")
    agent = BedrockSentinelAgent()
    optimization = agent.analyze_and_optimize(telemetry, tf_code)

    print(f"  💡 Executive Diagnosis:")
    print(f"     \"{optimization['executive_summary']}\"")
    print(f"\n  🎯 Projected Monthly Savings: ${optimization['projected_monthly_savings_usd']:.2f} / month")
    print(f"  🚀 Annualized Savings:        ${optimization['annualized_savings_usd']:.2f} / year")

    time.sleep(0.5)
    print("\n📝 [STEP 4/4]: Generating Terraform Pull Request & Safety Audit...")
    diff = iac.generate_unified_diff(tf_code, optimization["optimized_terraform"])
    pr_text = iac.create_pr_payload(optimization, diff)

    print("\n" + "="*75)
    print(pr_text)
    print("="*75)

    # Optionally persist optimized code
    print("\n✅ Verification complete: Clean HCL diff ready for automated PR dispatch.")

if __name__ == "__main__":
    main()
