variable "region" {
  type        = string
  default     = "us-east-1"
  description = "Default Aws Region for Infra"
}

variable "mlflow_namespace" {
  type        = string
  default     = ""
  description = "MLFLOW Namespace for deployment"
}

variable "mlflow_database_user" {
  type        = string
  sensitive   = true
  default     = ""
  description = "MLFLOW Database User"
}

variable "mlflow_database_password" {
  type        = string
  sensitive   = true
  default     = ""
  description = "MLFLOW Database Password"
}

variable "mlflow_database_db" {
  type        = string
  default     = "prod"
  description = "MLFLOW Database Name"
}

variable "mlflow_database_host" {
  type        = string
  default     = ""
  description = "MLFLOW Database Host"
}

variable "mlflow_artifact_bucket" {
  type        = string
  default     = ""
  description = "MLFLOW S3 Bucket for store ML artifacts"
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
