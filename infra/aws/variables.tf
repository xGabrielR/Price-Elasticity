variable "region" {
  type        = string
  default     = "us-east-1"
  description = "Default Aws Region for Infra"
}

variable "prefix" {
  type        = string
  default     = "ols"
  description = "Aws default prefix"
}

variable "eks_cluster_name" {
  type        = string
  default     = "ols-eks"
  description = "Default EKS Cluster name"
}

variable "bucket_names" {
  type        = list(string)
  description = "Aws default buckets"
  default = [
    "landing",  # dms data store
    "raw",      # bronze iceberg
    "trusted",  # silver iceberg
    "curated",  # gold iceberg
    "scripts",  # scripts and features
    "artifacts" # mlflow artifacts
  ]
}

locals {
  prefix = var.prefix
  common_tags = {
    Terraform   = true
    Environment = "dev"
  }
}