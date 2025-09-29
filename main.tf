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
