variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name for resource naming"
  type        = string
}

variable "environment" {
  description = "Environment (dev, staging, prod)"
  type        = string
}

variable "common_tags" {
  description = "Common tags for all resources"
  type        = map(string)
  default     = {}
}

# VPC Configuration
variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "enable_dns_hostnames" {
  description = "Enable DNS hostnames in VPC"
  type        = bool
  default     = true
}

variable "enable_dns_support" {
  description = "Enable DNS support in VPC"
  type        = bool
  default     = true
}

variable "public_subnets" {
  description = "List of public subnet configurations"
  type = list(object({
    name              = string
    cidr_block        = string
    availability_zone = string
  }))
  default = []
}

variable "private_subnets" {
  description = "List of private subnet configurations"
  type = list(object({
    name              = string
    cidr_block        = string
    availability_zone = string
  }))
  default = []
}

# Module Controls
variable "enable_vpc" {
  description = "Whether to create VPC resources"
  type        = bool
  default     = false
}




variable "services" {
  type = any
}