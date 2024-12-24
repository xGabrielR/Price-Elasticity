resource "kubernetes_namespace" "airflow" {
  metadata {
    name = var.airflow_namespace
  }
}

resource "kubernetes_namespace" "ingestion" {
  metadata {
    name = "ingestion"
  }
}

resource "kubectl_manifest" "airflow_github_credentials" {
  depends_on = [kubernetes_namespace.airflow]

  yaml_body = templatefile(
    "${path.module}/manifests/git-credentials-secret.yaml",
    {
      AIRFLOW_NAMESPACE        = var.airflow_namespace
      B64_GITHUB_USERNAME      = base64encode(var.airflow_github_username)
      B64_GITHUB_TOKEN_CLASSIC = base64encode(var.airflow_github_token_classic)
    }
  )
}

resource "kubectl_manifest" "airflow_fernet_key" {
  depends_on = [kubernetes_namespace.airflow]

  yaml_body = templatefile(
    "${path.module}/manifests/fernet-key.yaml",
    {
      AIRFLOW_NAMESPACE      = var.airflow_namespace
      B64_AIRFLOW_FERNET_KEY = base64encode(var.airflow_fernet_key)
    }
  )
}

resource "helm_release" "airflow" {
  name            = "airflow"
  replace         = true
  force_update    = true
  cleanup_on_fail = true
  lint            = true
  #recreate_pods   = true

  chart     = "${path.module}/helm"
  namespace = var.airflow_namespace

  depends_on = [
    kubernetes_namespace.airflow,
    kubectl_manifest.airflow_fernet_key,
    kubectl_manifest.airflow_github_credentials
  ]

  values = [
    "${file("${path.module}/helm/values.yaml")}"
  ]

  # Git Sync
  set {
    name  = "dags.gitSync.repo"
    value = var.airflow_dags_repo_url
  }

  set {
    name  = "dags.gitSync.subPath"
    value = "dags"
  }

  # Custom Params
  set {
    name  = "customParams.mlflow_tracking_server"
    value = var.mlflow_tracking_server
  }
  set {
    name  = "customParams.aws_access_key_id"
    value = var.aws_access_key_id
  }
  set {
    name  = "customParams.aws_secret_access_key"
    value = var.aws_secret_access_key
  }

  timeout = 1000
}