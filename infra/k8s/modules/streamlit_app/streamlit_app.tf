resource "kubernetes_namespace" "streamlit" {
  metadata {
    name = var.streamlit_namespace
  }
}

resource "kubectl_manifest" "streamlit_app_service" {
  depends_on = [kubernetes_namespace.streamlit]

  yaml_body = templatefile(
    "${path.module}/manifests/service.yaml",
    {
      STREAMLIT_NAMESPACE = var.streamlit_namespace
      STREAMLIT_APP_PORT  = var.streamlit_app_port
    }
  )
}

resource "kubectl_manifest" "mlflow_database_deployment" {
  depends_on = [kubernetes_namespace.streamlit]

  yaml_body = templatefile(
    "${path.module}/manifests/deployment.yaml",
    {
      STREAMLIT_NAMESPACE        = var.streamlit_namespace
      STREAMLIT_APP_PORT         = var.streamlit_app_port
      MLFLOW_TRACKING_SERVER     = var.mlflow_tracking_server
      STREAMLIT_APP_DOCKER_IMAGE = var.streamlit_app_docker_image
    }
  )
}