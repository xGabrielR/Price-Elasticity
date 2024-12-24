resource "kubernetes_namespace" "jupyter" {
  metadata {
    name = var.juptyer_namespace
  }
}

resource "kubectl_manifest" "mlflow_database_deployment" {
  depends_on = [
    kubernetes_namespace.jupyter
  ]

  yaml_body = templatefile(
    "${path.module}/manifests/pod.yaml",
    {
      MLFLOW_AWS_ACCESS_KEY_ID     = var.mlflow_s3_access_key_id
      MLFLOW_AWS_SECRET_ACCESS_KEY = var.mlflow_s3_secret_access_key
      MLFLOW_TRACKING_SERVER       = var.mlflow_tracking_server
      JUPYTER_NAMESPACE            = var.juptyer_namespace
    }
  )
}