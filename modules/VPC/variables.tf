variable "project_name" {
  description = "Name of the project"
  type        = string
}

variable "environment" {
  description = "Environment (dev, staging, prod)"
  type        = string
}

variable "region" {
  description = "AWS region"
  type        = string
}

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

variable "tags" {
  description = "Common tags for all resources"
  type        = map(string)
  default     = {}
}