from airflow import DAG
from airflow.models import Variable
from airflow.decorators import task, dag
from airflow.operators.empty import EmptyOperator
from airflow.providers.amazon.aws.operators.glue import GlueJobOperator
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator

from datetime import datetime, timedelta

SCRIPTS_BUCKET_NAME = "ols-lh-scripts"
LANDING_BUCKET_NAME = "ols-lh-landing"
RAW_BUCKET_NAME     = "ols-lh-raw"
TRUSTED_BUCKET_NAME = "ols-lh-trusted"
CURATED_BUCKET_NAME = "ols-lh-curated"

RAW_GLUE_DATABASE_NAME = "ols_lh_raw"
TRUSTED_GLUE_DATABASE_NAME = "ols_lh_trusted"
CURATED_GLUE_DATABASE_NAME = "ols_lh_curated"

DEFAULT_GLUE_IAM_ROLE = "ols-glue-role"
DEFAULT_GLUE_SCRIPT_PATH = f"s3://{SCRIPTS_BUCKET_NAME}/glue_jobs/main.py"
DEFAULT_GLUE_CATALOG_NAME = "catalog"
DEFAULT_GLUE_MARKETPLACE_ICEBERG_CONN_NAME = "iceberg_conn"
DEFAULT_ICEBERG_WAREHOUSE_PATH = f"s3://{RAW_BUCKET_NAME}/"

GLUE_JOB_ARGS = {
    "--job-language": "python",
    "--enable-job-insights": "false",
    "--conf": f"spark.sql.catalog.{DEFAULT_GLUE_CATALOG_NAME}=org.apache.iceberg.spark.SparkCatalog " + \
            f"--conf spark.sql.catalog.{DEFAULT_GLUE_CATALOG_NAME}.warehouse={DEFAULT_ICEBERG_WAREHOUSE_PATH} " + \
            f"--conf spark.sql.catalog.{DEFAULT_GLUE_CATALOG_NAME}.catalog-impl=org.apache.iceberg.aws.glue.GlueCatalog " + \
            f"--conf spark.sql.catalog.{DEFAULT_GLUE_CATALOG_NAME}.io-impl=org.apache.iceberg.aws.s3.S3FileIO " + \
            f"--conf spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions " + \
            f"--conf spark.sql.parquet.int96RebaseModeInRead=CORRECTED " + \
            f"--conf spark.sql.parquet.int96RebaseModeInWrite=CORRECTED " + \
            f"--conf spark.sql.parquet.datetimeRebaseModeInRead=CORRECTED " + \
            f"--conf spark.sql.parquet.datetimeRebaseModeInWrite=CORRECTED",
    "--PROJECT_PREFIX": "ols",
    "--S3_BUCKET_LANDING": LANDING_BUCKET_NAME,
    "--S3_BUCKET_RAW": RAW_BUCKET_NAME,
    "--S3_BUCKET_TRUSTED": TRUSTED_BUCKET_NAME,
    "--S3_BUCKET_CURATED": CURATED_BUCKET_NAME,
    "--GLUE_DATABASE_RAW": RAW_GLUE_DATABASE_NAME,
    "--GLUE_DATABASE_TRUSTED": TRUSTED_GLUE_DATABASE_NAME,
    "--GLUE_DATABASE_CURATED": CURATED_GLUE_DATABASE_NAME
}

GLUE_JOB_KWARGS = {
    "GlueVersion": "4.0",
    "NumberOfWorkers": 2,
    "WorkerType": "G.1X",
    "Connections": {
        "Connections":
            [DEFAULT_GLUE_MARKETPLACE_ICEBERG_CONN_NAME]
    }
}

DEFAULT_ARGS = {
    "retries": 0,
    "depends_on_past": False,
    "start_date": datetime(2018, 1, 1),
}

@dag(
    catchup=True,
    max_active_runs=1,
    default_args=DEFAULT_ARGS,
    schedule_interval="0 0 * * 0", # Every Sunday
    dagrun_timeout=timedelta(minutes=120),
    description="Workflow Processing Data Engineering & Retrain Price Elasticity OLS",
)
def OLIST_ML_WORKFLOW():
    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")

    pod_python_extractor = EmptyOperator(
        task_id="pod_python_extractor"
    )

    glue_job_processing = GlueJobOperator(
        task_id="glue_job_processing",
        job_name="glue_job_processing",
        region_name="us-east-1",
        script_args=GLUE_JOB_ARGS,
        iam_role_name=DEFAULT_GLUE_IAM_ROLE,
        script_location=DEFAULT_GLUE_SCRIPT_PATH,
        create_job_kwargs=GLUE_JOB_KWARGS,
    )

    pod_price_elasticity_retrain = KubernetesPodOperator(
        task_id="pod_price_elasticity_retrain",
        in_cluster=True,
        namespace="ingestion",
        image="gabrielrichter/price_elasticity_retrain:1",
        name=f"price_elasticity_retrain",
        random_name_suffix=True,
        reattach_on_restart=True,
        is_delete_operator_pod=True,
        image_pull_policy="Always",
        get_logs=True,
        log_events_on_failure=False,
        env_vars={
            "TRAIN_DATE": "{{ execution_date.strftime('%Y-%m-%d') }}",
            "MLFLOW_TRACKING_SERVER": Variable.get("MLFLOW_TRACKING_SERVER"),
            "AWS_ACCESS_KEY_ID": Variable.get("AWS_ACCESS_KEY_ID"),
            "AWS_SECRET_ACCESS_KEY": Variable.get("AWS_SECRET_ACCESS_KEY"),
        }
    )  

    start >> pod_python_extractor >> glue_job_processing >> pod_price_elasticity_retrain >> end


OLIST_ML_WORKFLOW()