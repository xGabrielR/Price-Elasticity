resource "aws_glue_catalog_database" "bronze" {
  name = "${var.prefix}_lh_raw"
  tags = local.common_tags
}

resource "aws_glue_catalog_database" "silver" {
  name = "${var.prefix}_lh_trusted"
  tags = local.common_tags
}

resource "aws_glue_catalog_database" "gold" {
  name = "${var.prefix}_lh_curated"
  tags = local.common_tags
}

resource "aws_s3_object" "glue_main_job" {
  bucket = "ols-lh-scripts"
  key    = "glue_jobs/main.py"
  source = "./glue_jobs/main.py"

  depends_on = [aws_s3_bucket.buckets]
}
