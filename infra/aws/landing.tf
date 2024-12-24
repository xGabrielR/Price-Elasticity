resource "aws_s3_object" "order_item" {
  bucket = "ols-lh-landing"
  key    = "oltp/prod/order_item/order_item.parquet"
  source = "./landing/order_item.parquet"

  depends_on = [aws_s3_bucket.buckets]
}

resource "aws_s3_object" "order" {
  bucket = "ols-lh-landing"
  key    = "oltp/prod/order/order.parquet"
  source = "./landing/order.parquet"

  depends_on = [aws_s3_bucket.buckets]
}