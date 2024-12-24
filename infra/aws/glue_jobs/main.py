import sys
from pytz import timezone
from datetime import datetime

from awsglue.job import Job
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.utils import getResolvedOptions

SOURCE_SCHEMA_TABLES = [
    "oltp_prod_order",
    "oltp_prod_order_item"
]

RAW_TRUSTED = {
    "oltp_prod_order": """
        SELECT 
            order_id,
            customer_id,
            UPPER(TRIM(order_status)) AS order_status,
            TO_TIMESTAMP(order_approved_at) AS order_approved_at,
            TO_TIMESTAMP(order_delivered_carrier_date) AS order_delivered_carrier_date,
            TO_TIMESTAMP(order_delivered_customer_date) AS order_delivered_customer_date,
            TO_TIMESTAMP(order_estimated_delivery_date) AS order_estimated_delivery_date,
            TO_TIMESTAMP(order_purchase_timestamp) AS order_purchase_timestamp
        FROM {source_schema_table}
    """,
    "oltp_prod_order_item": """
        SELECT 
            order_id,
            order_item_id,
            product_id,
            seller_id,
            CAST(price AS DOUBLE) AS price,
            CAST(freight_value AS DOUBLE) AS freight_value,
            TO_TIMESTAMP(shipping_limit_date) AS shipping_limit_date
        FROM {source_schema_table}
    """
}

def create_or_replace_iceberg_table(
    df,
    glue_database: str,
    source_schema_table: str,
) -> None:
    df.coalesce(1).writeTo(f"catalog.{glue_database}.{source_schema_table}")\
        .using("iceberg")\
        .tableProperty("write.format.default", "parquet")\
        .tableProperty("write.distribution-mode", "hash")\
        .tableProperty("write.parquet.dict-size-bytes", "134217728")\
        .createOrReplace()
    

if __name__ == "__main__":
    args = getResolvedOptions(
        sys.argv,
        [
            "JOB_NAME",
            "S3_BUCKET_LANDING",
            "S3_BUCKET_RAW",
            "S3_BUCKET_TRUSTED",
            "S3_BUCKET_CURATED",
            "GLUE_DATABASE_RAW",
            "GLUE_DATABASE_TRUSTED",
            "GLUE_DATABASE_CURATED"
        ]
    )

    print(args)
    print("\n")
    print(f"START SPARK JOB AT: {datetime.now(timezone('America/Sao_Paulo'))}")

    # Setup Spark
    sc = SparkContext()
    glueContext = GlueContext(sc)
    spark = glueContext.spark_session
    job = Job(glueContext)
    job.init(args["JOB_NAME"], args)

    # Landing to Raw
    for source_schema_table in SOURCE_SCHEMA_TABLES:
        print(f"[{datetime.now(timezone('America/Sao_Paulo'))}] [START] [LANDING - RAW] {source_schema_table}")
        
        source, schema, table = source_schema_table.split("_")[0], source_schema_table.split("_")[1], '_'.join(source_schema_table.split("_")[2:])
        
        df = spark.read.format("parquet").load(f"s3a://{args['S3_BUCKET_LANDING']}/{source}/{schema}/{table}")

        create_or_replace_iceberg_table(
            df=df,
            glue_database=args['GLUE_DATABASE_RAW'],
            source_schema_table=source_schema_table
        )
        
        print(f"[{datetime.now(timezone('America/Sao_Paulo'))}] [ENDED] [LANDING - RAW] {source_schema_table}")

    # Raw to Trusted
    for source_schema_table, query in RAW_TRUSTED.items():
        print(f"[{datetime.now(timezone('America/Sao_Paulo'))}] [START] [RAW - TRUSTED] {source_schema_table}")

        create_or_replace_iceberg_table(
            df=spark.sql(
                query.format(
                    source_schema_table=f"catalog.{args['GLUE_DATABASE_RAW']}.{source_schema_table}"
                )
            ),
            glue_database=args["GLUE_DATABASE_TRUSTED"],
            source_schema_table=source_schema_table
        )

        print(f"[{datetime.now(timezone('America/Sao_Paulo'))}] [ENDED] [RAW - TRUSTED] {source_schema_table}")

    print(f"FINISH SPARK JOB AT: {datetime.now(timezone('America/Sao_Paulo'))}")
