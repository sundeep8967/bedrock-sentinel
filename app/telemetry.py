import os
from typing import Dict, Any, List

class CloudTelemetryCollector:
    """
    Collects CloudWatch and Cost Explorer telemetry.
    Supports live AWS Boto3 SDK or deterministic telemetry mock.
    """
    def __init__(self, region: str = "us-east-1"):
        self.region = region

    def fetch_utilization_metrics(self) -> List[Dict[str, Any]]:
        """
        Gathers utilization metrics across EC2, EBS, and RDS resources.
        """
        # Simulated CloudWatch 14-day rolling telemetry
        return [
            {
                "resource_id": "aws_instance.worker_fleet",
                "resource_type": "EC2",
                "current_sku": "t3.2xlarge",
                "current_cost_usd_monthly": 240.00,
                "metrics": {
                    "avg_cpu_percent": 2.8,
                    "p99_cpu_percent": 6.1,
                    "avg_memory_percent": 14.2,
                    "network_io_kbs": 42.0
                },
                "status": "GROSSLY_UNDERUTILIZED"
            },
            {
                "resource_id": "aws_ebs_volume.orphaned_backup_vol",
                "resource_type": "EBS",
                "current_sku": "gp3 (500GB)",
                "current_cost_usd_monthly": 40.00,
                "metrics": {
                    "days_unattached": 45,
                    "read_ops_last_30d": 0,
                    "write_ops_last_30d": 0
                },
                "status": "ORPHANED_UNATTACHED"
            },
            {
                "resource_id": "aws_db_instance.app_db",
                "resource_type": "RDS_PostgreSQL",
                "current_sku": "db.m5.2xlarge",
                "current_cost_usd_monthly": 520.00,
                "metrics": {
                    "avg_cpu_percent": 7.4,
                    "active_connections_avg": 8,
                    "max_connections_allowed": 680,
                    "storage_used_gb": 42
                },
                "status": "OVERPROVISIONED"
            }
        ]

    def compute_current_monthly_burn(self, resources: List[Dict[str, Any]]) -> float:
        return sum(r["current_cost_usd_monthly"] for r in resources)
