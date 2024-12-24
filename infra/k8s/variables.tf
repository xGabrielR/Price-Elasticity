variable "region" {
  type        = string
  default     = "us-east-1"
  description = "Default Aws Region for Infra"
}

# ------------------
# MLFLOW
# ------------------

variable "mlflow_namespace" {
  type        = string
  default     = "mlflow"
  description = "MLFLOW Namespace for deployment"
}

variable "mlflow_database_user" {
  type        = string
  sensitive   = true
  default     = "admin123"
  description = "MLFLOW Database User"
}

variable "mlflow_database_password" {
  type        = string
  sensitive   = true
  default     = "admin123"
  description = "MLFLOW Database Password"
}

variable "mlflow_database_db" {
  type        = string
  default     = "prod"
  description = "MLFLOW Database Name"
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
  description = "MLFLOW Secret Access Key for S3 Bucket ML artifacts"
}

# ------------------
# STREAMLIT
# ------------------

variable "streamlit_namespace" {
  type        = string
  default     = "streamlit"
  description = "K8s Namespace for Streamlit deployment"
}

variable "streamlit_app_port" {
  type        = number
  default     = 8501
  description = "STREAMLIT APP port"
}

variable "streamlit_app_docker_image" {
  type        = string
  default     = "gabrielrichter/streamlit_app:1"
  description = "STREAMLIT Docker App Image"
}

# ------------------
# AIRFLOW
# ------------------

variable "airflow_namespace" {
  type        = string
  default     = "airflow"
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


variable "host" {
  type = string
}

variable "client_certificate" {
  type = string
}

variable "client_key" {
  type = string
}

variable "cluster_ca_certificate" {
  type = string
}