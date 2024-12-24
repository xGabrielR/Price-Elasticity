resource "kubernetes_namespace" "mlflow" {
  metadata {
    name = var.mlflow_namespace
  }
}

resource "kubectl_manifest" "mlflow_database_service" {
  depends_on = [kubernetes_namespace.mlflow]
  yaml_body  = file("${path.module}/manifests/service.yaml")
}

resource "kubectl_manifest" "mlflow_database_pv" {
  depends_on = [kubernetes_namespace.mlflow]
  yaml_body  = file("${path.module}/manifests/pv.yaml")
}

resource "kubectl_manifest" "mlflow_database_pvc" {
  depends_on = [
    kubernetes_namespace.mlflow,
    kubectl_manifest.mlflow_database_pv
  ]

  yaml_body = file("${path.module}/manifests/pvc.yaml")
}

resource "kubectl_manifest" "mlflow_database_deployment" {
  depends_on = [
    kubernetes_namespace.mlflow,
    kubectl_manifest.mlflow_database_pvc
  ]

  yaml_body = templatefile(
    "${path.module}/manifests/deployment.yaml",
    {
      MLFLOW_DATABASE_USER     = var.mlflow_database_user
      MLFLOW_DATABASE_PASSWORD = var.mlflow_database_password
      MLFLOW_DATABASE_DB       = var.mlflow_database_db
    }
  )
}