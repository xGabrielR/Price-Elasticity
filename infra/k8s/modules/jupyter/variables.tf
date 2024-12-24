variable "region" {
  type        = string
  default     = "us-east-1"
  description = "Default Aws Region for Infra"
}

variable "juptyer_namespace" {
  type        = string
  default     = "notebook"
  description = "JUPYTER Notebook Namespace"
}

variable "mlflow_tracking_server" {
  type        = string
  default     = ""
  description = "MLFLOW Tracking Server"
}

variable "mlflow_s3_access_key_id" {
  type        = string
  sensitive   = true
  default     = ""
  description = "MLFLOW Access Key for S3 Bucket ML artifacts"
}

variable "mlflow_s3_secret_access_key" {
  type        = string
  sensitive   = true
  default     = ""
  description = "MLFLOW Access Key for S3 Bucket ML artifacts"
}

