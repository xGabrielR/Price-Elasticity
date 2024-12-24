module "postgres_mlflow" {
  source                   = "./modules/postgres_mlflow"
  region                   = var.region
  mlflow_namespace         = var.mlflow_namespace
  mlflow_database_user     = var.mlflow_database_user
  mlflow_database_password = var.mlflow_database_password
  mlflow_database_db       = var.mlflow_database_db
}

module "server_mlflow" {
  source                      = "./modules/server_mlflow"
  depends_on                  = [module.postgres_mlflow]
  region                      = var.region
  mlflow_namespace            = var.mlflow_namespace
  mlflow_database_user        = var.mlflow_database_user
  mlflow_database_password    = var.mlflow_database_password
  mlflow_database_db          = var.mlflow_database_db
  mlflow_database_host        = "mlflow-database-svc.${var.mlflow_namespace}.svc.Cluster.local"
  mlflow_artifact_bucket      = var.mlflow_artifact_bucket
  mlflow_s3_access_key_id     = var.mlflow_s3_access_key_id
  mlflow_s3_secret_access_key = var.mlflow_s3_secret_access_key
}

module "airflow" {
  source                       = "./modules/airflow"
  region                       = var.region
  airflow_namespace            = var.airflow_namespace
  airflow_fernet_key           = var.airflow_fernet_key
  airflow_dags_repo_url        = var.airflow_dags_repo_url
  airflow_github_username      = var.airflow_github_username
  airflow_github_token_classic = var.airflow_github_token_classic

  # Custom Params - Airflow Variables
  mlflow_tracking_server = "http://server-mlflow.${var.mlflow_namespace}.svc.cluster.local:5000"
  aws_access_key_id      = var.mlflow_s3_access_key_id
  aws_secret_access_key  = var.mlflow_s3_secret_access_key
}

module "streamlit_app" {
  source                     = "./modules/streamlit_app"
  depends_on                 = [module.server_mlflow]
  region                     = var.region
  streamlit_namespace        = var.streamlit_namespace
  streamlit_app_port         = var.streamlit_app_port
  streamlit_app_docker_image = var.streamlit_app_docker_image
  mlflow_tracking_server     = "http://server-mlflow.${var.mlflow_namespace}.svc.cluster.local:5000"
}

module "jupyter_notebook" {
  source                      = "./modules/jupyter"
  region                      = var.region
  juptyer_namespace           = "notebook"
  mlflow_s3_access_key_id     = var.mlflow_s3_access_key_id
  mlflow_s3_secret_access_key = var.mlflow_s3_secret_access_key
  mlflow_tracking_server      = "http://server-mlflow.${var.mlflow_namespace}.svc.cluster.local:5000"
}