variable "project_name" {
  description = "Name of the project"
  type        = string
}

variable "environment" {
  description = "Environment (dev, staging, prod)"
  type        = string
}

variable "vpc_id" {
  description = "ID of the VPC"
  type        = string
}

variable "security_groups" {
  description = "List of security group configurations"
  type = list(object({
    name        = string
    description = string
    ingress_rules = list(object({
      from_port   = number
      to_port     = number
      protocol    = string
      cidr_blocks = list(string)
      description = optional(string, "")
    }))
    egress_rules = optional(list(object({
      from_port   = number
      to_port     = number
      protocol    = string
      cidr_blocks = list(string)
      description = optional(string, "")
    })), [])
  }))
  default = []
}

variable "tags" {
  description = "Common tags for all resources"
  type        = map(string)
  default     = {}
}
