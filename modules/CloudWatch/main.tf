resource "aws_cloudwatch_log_group" "this" {
  name              = "/app/${var.name}"
  retention_in_days = var.retention_days
}
