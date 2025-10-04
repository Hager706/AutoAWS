resource "aws_route53_record" "this" {
  count   = var.create ? 1 : 0
  zone_id = var.zone_id
  name    = var.record_name
  type    = "A"

  alias {
    name                   = var.alb_dns
    zone_id                = var.alb_zone_id
    evaluate_target_health = true
  }
}
