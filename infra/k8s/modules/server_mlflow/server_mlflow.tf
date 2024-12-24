resource "helm_release" "airflow" {
  name            = "server"
  replace         = true
  force_update    = true
  cleanup_on_fail = true
  lint            = true

  chart     = "${path.module}/helm"
  namespace = var.mlflow_namespace

  values = [
    "${file("${path.module}/helm/values.yaml")}"
  ]

  # Postgres Connection
  set {
    name  = "backendStore.postgres.host"
    value = var.mlflow_database_host
  }

  set {
    name  = "backendStore.postgres.database"
    value = var.mlflow_database_db
  }

  set {
    name  = "backendStore.postgres.user"
    value = var.mlflow_database_user
  }

  set {
    name  = "backendStore.postgres.password"
    value = var.mlflow_database_password
  }

  # S3 Connection
  set {
    name  = "artifactRoot.s3.bucket"
    value = var.mlflow_artifact_bucket
  }

  set {
    name  = "artifactRoot.s3.awsAccessKeyId"
    value = var.mlflow_s3_access_key_id
  }

  set {
    name  = "artifactRoot.s3.awsSecretAccessKey"
    value = var.mlflow_s3_secret_access_key
  }

  timeout = 1000
}