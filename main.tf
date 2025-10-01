# VPC Module
module "vpc" {
  count  = var.enable_vpc ? 1 : 0
  source = "./modules/VPC"

  project_name         = var.project_name
  environment          = var.environment
  vpc_cidr             = var.vpc_cidr
  enable_dns_hostnames = var.enable_dns_hostnames
  enable_dns_support   = var.enable_dns_support
  public_subnets       = var.public_subnets
  private_subnets      = var.private_subnets
  tags                 = var.common_tags
  region               = var.aws_region

}


module "security_groups" {
  source          = "./modules/Security_groups"
  project_name    = var.project_name
  environment     = var.environment
  vpc_id          = var.enable_vpc ? module.vpc[0].vpc_id : null
  security_groups = var.services.security_groups
  tags            = var.common_tags
}


module "alb" {
  source            = "./modules/alb"
  name              = var.project_name
  vpc_id            = module.vpc[0].vpc_id
  public_subnet_ids = module.vpc[0].public_subnet_ids
  alb_sg_id         = module.security_groups.security_group_ids["alb"]
}


# --- IAM ---
module "iam" {
  source = "./modules/iam"
  name   = var.project_name
}


# Autoscaling (launch template + ASG)
module "autoscaling" {
  source                = "./modules/autoscaling"
  name                  = var.project_name
  ami                   = try(var.services.autoscaling.ami, "")
  instance_type         = try(var.services.autoscaling.instance_type, "t3.micro")
  app_sg_id             = module.security_groups.security_group_ids["app"]
  subnet_ids            = module.vpc[0].private_subnet_ids
  min_size              = try(var.services.autoscaling.min_size, 1)
  max_size              = try(var.services.autoscaling.max_size, 1)
  user_data             = try(var.services.autoscaling.user_data, "")
  instance_profile_name = module.iam.instance_profile_name
  target_group_arn      = module.alb.target_group_arn
}

# Monitoring (CloudWatch log group)
module "monitoring" {
  source         = "./modules/CloudWatch"
  name           = var.project_name
  retention_days = try(var.services.monitoring.retention_days, 7)
}


# S3
module "s3" {
  source      = "./modules/S3"
  bucket_name = var.project_name
  env         = var.environment
  versioning  = try(var.services.s3.versioning, false)
  tags        = var.common_tags
}


# RDS (optional)
module "rds" {
  source            = "./modules/RDS"
  create            = try(var.services.rds.create, false)
  name              = var.project_name
  engine            = try(var.services.rds.engine, "mysql")
  engine_version    = try(var.services.rds.engine_version, null)
  instance_class    = try(var.services.rds.instance_class, "db.t3.micro")
  allocated_storage = try(var.services.rds.allocated_storage, 20)
  db_name           = try(var.services.rds.db_name, null)
  username          = try(var.services.rds.username, null)
  password          = try(var.services.rds.password, null)
  subnet_ids        = module.vpc.private_subnet_ids
  db_sg_id          = module.security_groups.security_group_ids["app"]
}


# Route53 (optional)
module "route53" {
  source      = "./modules/route53"
  create      = try(var.services.route53.create, false)
  zone_id     = try(var.services.route53.zone_id, "")
  record_name = try(var.services.route53.record_name, "")
  alb_dns     = module.alb.dns_name
  alb_zone_id = module.alb.dns_zone_id
}