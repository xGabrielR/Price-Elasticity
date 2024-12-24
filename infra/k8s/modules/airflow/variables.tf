variable "region" {
  type        = string
  default     = "us-east-1"
  description = "Default Aws Region for Infra"
}

variable "airflow_namespace" {
  type        = string
  default     = ""
  description = "AIRFLOW Namespace for deployment"
}

variable "airflow_fernet_key" {
  type        = string
  sensitive   = true
  default     = ""
  description = "AIRFLOW Random Fernet Key"
}

variable "airflow_dags_repo_url" {
  type        = string
  default     = ""
  description = "AIRFLOW GitSync Repo URL"
}

variable "airflow_github_username" {
  type        = string
  sensitive   = true
  default     = ""
  description = "AIRFLOW GitSync Github Username"
}

variable "airflow_github_token_classic" {
  type        = string
  sensitive   = true
  default     = ""
  description = "AIRFLOW GitSync Github Token"
}

variable "mlflow_tracking_server" {
  type        = string
  sensitive   = true
  default     = ""
  description = "MLFLOW Tracking Server"
}

variable "aws_access_key_id" {
  type        = string
  sensitive   = true
  default     = ""
  description = "Aws Access Key with Access to AWS glue Catalog and Jobs"
}

variable "aws_secret_access_key" {
  type        = string
  sensitive   = true
  default     = ""
  description = "Aws Secret Access with Access to AWS glue Catalog and Jobs"
}