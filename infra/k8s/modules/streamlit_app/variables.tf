variable "region" {
  type        = string
  default     = "us-east-1"
  description = "Default Aws Region for Infra"
}

variable "streamlit_namespace" {
  type        = string
  default     = "streamlit"
  description = "K8s Namespace for Streamlit deployment"
}

variable "streamlit_app_port" {
  type        = number
  default     = 0
  description = "STREAMLIT APP port"
}

variable "streamlit_app_docker_image" {
  type        = string
  default     = ""
  description = "STREAMLIT Docker App Image"
}

variable "mlflow_tracking_server" {
  type        = string
  default     = ""
  description = "MLFLOW Tracking Server for Streamlit App"
}