output "vpc_id" {
  description = "VPC ID"
  value       = var.enable_vpc ? module.vpc[0].vpc_id : null
}

output "public_subnet_ids" {
  description = "Public subnet IDs"
  value       = var.enable_vpc ? module.vpc[0].public_subnet_ids : []
}

output "private_subnet_ids" {
  description = "Private subnet IDs"
  value       = var.enable_vpc ? module.vpc[0].private_subnet_ids : []
}

output "security_groups" {
  value = module.security_groups.security_group_ids
}

output "alb_dns" {
  value = module.alb.dns_name
}

output "s3_bucket" {
  value = module.s3.bucket_name
}


output "rds_endpoint" {
  value = try(module.rds.endpoint, null)
}