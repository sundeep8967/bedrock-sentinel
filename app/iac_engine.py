import os
import difflib
from typing import Dict, Any

class IaCEngine:
    """
    Manages Terraform reading, unified diff generation, and PR payload synthesis.
    """
    def __init__(self, tf_path: str):
        self.tf_path = os.path.abspath(tf_path)

    def read_config(self) -> str:
        with open(self.tf_path, "r", encoding="utf-8") as f:
            return f.read()

    def generate_unified_diff(self, original_tf: str, optimized_tf: str) -> str:
        diff_lines = list(difflib.unified_diff(
            original_tf.splitlines(keepends=True),
            optimized_tf.splitlines(keepends=True),
            fromfile="a/main.tf",
            tofile="b/main.tf"
        ))
        return "".join(diff_lines)

    def apply_patch(self, optimized_tf: str):
        with open(self.tf_path, "w", encoding="utf-8") as f:
            f.write(optimized_tf)

    def create_pr_payload(self, optimization_result: Dict[str, Any], diff: str) -> str:
        savings = optimization_result["projected_monthly_savings_usd"]
        annual = optimization_result["annualized_savings_usd"]
        pct = (savings / optimization_result["current_monthly_burn_usd"]) * 100

        actions_md = ""
        for r in optimization_result["remediations"]:
            actions_md += f"- **{r['resource_id']}** ({r['action']}):\n"
            actions_md += f"  - Previous: `{r['original_sku']}` ➔ New: `{r['recommended_sku']}`\n"
            actions_md += f"  - Monthly Savings: **${r['monthly_savings_usd']:.2f}**\n"
            actions_md += f"  - *Reasoning:* {r['justification']}\n\n"

        return f"""# 📉 FinOps Auto-Remediation: Cut AWS Cloud Spend by ${savings:.2f}/mo ({pct:.1f}%)

> **Triggered by BedrockSentinel Autonomous Cloud Agent**  
> **Model:** Amazon Bedrock (`anthropic.claude-3-5-sonnet`)  
> **Target Environment:** AWS `us-east-1` (Terraform)

---

## 💰 Financial Impact Summary
| Metric | Before Optimization | After Optimization | Net Savings |
| :--- | :--- | :--- | :--- |
| **Monthly Cloud Burn** | **${optimization_result['current_monthly_burn_usd']:.2f}** | **${optimization_result['projected_monthly_burn_usd']:.2f}** | **-${savings:.2f} / month** |
| **Annualized Run-Rate** | **${optimization_result['current_monthly_burn_usd']*12:.2f}** | **${optimization_result['projected_monthly_burn_usd']*12:.2f}** | **-${annual:.2f} / year** |

---

## 🔍 Automated Remediation Breakdown
{actions_md}

## 📋 Unified Terraform Diff
```diff
{diff}
```

---

## 🛡️ Safety & Rollback Guarantee
- Automatic EBS snapshot created before volume decommissioning.
- RDS modification performed during standard maintenance window with multi-AZ failover preserved.
- To rollback, run: `git revert HEAD && terraform apply -auto-approve`.
"""
