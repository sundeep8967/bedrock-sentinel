# Terraform Configuration with typical AWS FinOps Anti-Patterns
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

# 1. Oversized EC2 Worker Instance (Avg CPU: 2.8%, Memory: 14%)
resource "aws_instance" "worker_fleet" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.2xlarge"  # Expensive: ~$240/mo, grossly underutilized
  tags = {
    Name        = "analytics-worker-primary"
    Environment = "production"
    ManagedBy   = "Terraform"
  }
}

# 2. Abandoned Orphaned EBS Volume (Unattached for 45 days)
resource "aws_ebs_volume" "orphaned_backup_vol" {
  availability_zone = "us-east-1a"
  size              = 500       # 500 GB gp3 costing ~$40/mo unattached
  type              = "gp3"
  iops              = 3000
  throughput        = 125
  tags = {
    Name = "temp-db-snapshot-unattached"
  }
}

# 3. Oversized RDS Database Instance
resource "aws_db_instance" "app_db" {
  identifier        = "app-production-db"
  allocated_storage = 200
  engine            = "postgres"
  engine_version    = "15.4"
  instance_class    = "db.m5.2xlarge" # ~$520/mo with minimal connection pool
  username          = "dbadmin"
  password          = "SuperSecretPassword123!"
  skip_final_snapshot = true
}
