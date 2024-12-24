variable "region" {
  type        = string
  default     = "us-east-1"
  description = "Default Aws Region for Infra"
}

variable "mlflow_namespace" {
  type        = string
  default     = "mlflow"
  description = "K8s Namespace for MLFLOW deployment"
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
