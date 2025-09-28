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

}